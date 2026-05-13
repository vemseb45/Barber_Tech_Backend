from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from datetime import timedelta
from cita.models import Cita
from usuarios.models import Usuario

class AdminAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        time_range = request.query_params.get('timeRange', 'Últimos 30 días')
        
        now = timezone.now()
        start_date = now - timedelta(days=30)
        
        if time_range == 'Mes anterior':
            start_date = now.replace(day=1) - timedelta(days=1)
            start_date = start_date.replace(day=1)
            now = now.replace(day=1) - timedelta(days=1)
        elif time_range == 'Este año':
            start_date = now.replace(month=1, day=1)
        
        # Filtramos citas completadas en el rango de tiempo
        citas_completadas = Cita.objects.filter(estado='CONF', fecha__gte=start_date, fecha__lte=now)

        # 1. Total Ganado
        total_ganado = citas_completadas.aggregate(total=Sum('servicio__precio'))['total'] or 0

        # 2. Clientes Nuevos
        clientes_nuevos = Usuario.objects.filter(rol='Cliente', date_joined__gte=start_date, date_joined__lte=now).count()

        # 3. Valor promedio por día
        days_in_range = (now - start_date).days or 1
        valor_promedio_dia = float(total_ganado) / days_in_range

        # 4. Servicios más populares
        servicios_qs = citas_completadas.values('servicio__nombre').annotate(count=Count('id')).order_by('-count')[:4]
        total_citas_count = citas_completadas.count() or 1
        
        popular_services = []
        colors = ['bg-[#5213fc]', 'bg-purple-500', 'bg-blue-500', 'bg-slate-400']
        for idx, svc in enumerate(servicios_qs):
            porcentaje = (svc['count'] / total_citas_count) * 100
            popular_services.append({
                'name': svc['servicio__nombre'],
                'value': round(porcentaje),
                'color': colors[idx % len(colors)]
            })

        # 5. Desempeño de Barberos
        # Filtrar solo barberos
        barberos = Usuario.objects.filter(rol='Barbero')
        barbers_performance = []
        
        for barbero in barberos:
            # Todas las citas del barbero en el rango
            citas_barbero = Cita.objects.filter(cedula_barbero=barbero, fecha__gte=start_date, fecha__lte=now)
            total_citas = citas_barbero.count()
            citas_conf = citas_barbero.filter(estado='CONF')
            completadas = citas_conf.count()
            
            if total_citas == 0:
                continue

            ingresos = citas_conf.aggregate(total=Sum('servicio__precio'))['total'] or 0
            
            rating_aggr = citas_conf.filter(calificacion__isnull=False).aggregate(avg=Avg('calificacion__puntuacion'))['avg']
            rating = round(rating_aggr, 1) if rating_aggr else 5.0

            nombre_completo = f"{barbero.first_name} {barbero.last_name}".strip()
            
            barbers_performance.append({
                'name': nombre_completo if nombre_completo else barbero.username,
                'role': 'Barbero Profesional',
                'citas': total_citas,
                'completadas': completadas,
                'rating': rating,
                'ingresos': float(ingresos),
                'avatar': f'https://ui-avatars.com/api/?name={barbero.first_name or barbero.username}&background=random'
            })

        # 6. Ingresos Mensuales (Chart Data)
        chart_labels = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        current_month = now.month
        months_to_show = 7
        
        recent_labels = []
        recent_data = []
        
        for i in range(months_to_show - 1, -1, -1):
            m = current_month - i
            y = now.year
            if m <= 0:
                m += 12
                y -= 1
            
            citas_mes = Cita.objects.filter(estado='CONF', fecha__month=m, fecha__year=y)
            ingresos_mes = citas_mes.aggregate(total=Sum('servicio__precio'))['total'] or 0
            
            recent_labels.append(chart_labels[m-1])
            recent_data.append(float(ingresos_mes))
            
        max_ingreso = max(recent_data) if recent_data and max(recent_data) > 0 else 1
        chart_percentages = [round((val / max_ingreso) * 100) for val in recent_data]

        return Response({
            "success": True,
            "data": {
                "total_ganado": float(total_ganado),
                "clientes_nuevos": clientes_nuevos,
                "valor_promedio_dia": float(valor_promedio_dia),
                "popular_services": popular_services,
                "barbers_performance": barbers_performance,
                "chart_data": chart_percentages,
                "chart_labels": recent_labels
            }
        })
