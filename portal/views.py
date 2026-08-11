import io
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import MaterialIssue, MaterialConsumption, DPR, Expense


@login_required
def dashboard(request):
    total_material_issued = MaterialIssue.objects.aggregate(total=Sum('issued_quantity'))['total'] or 0
    total_material_consumed = MaterialConsumption.objects.aggregate(total=Sum('installed_quantity'))['total'] or 0
    total_material_remaining = MaterialConsumption.objects.aggregate(total=Sum('remaining_quantity'))['total'] or 0
    total_expenses = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0

    all_dpr = DPR.objects.values('person').annotate(
        rfc=Sum('rfc_quantity'),
        ng=Sum('ng_quantity'),
        tf=Sum('tf_quantity'),
        gi=Sum('gi_quantity')
    )
    labels = [entry['person'] for entry in all_dpr]
    daily_performance = {
        'labels': labels,
        'rfc': [float(entry['rfc'] or 0) for entry in all_dpr],
        'ng': [float(entry['ng'] or 0) for entry in all_dpr],
        'tf': [float(entry['tf'] or 0) for entry in all_dpr],
        'gi': [float(entry['gi'] or 0) for entry in all_dpr],
    }

    context = {
        'total_material_issued': total_material_issued,
        'total_material_consumed': total_material_consumed,
        'total_material_remaining': total_material_remaining,
        'total_expenses': total_expenses,
        'daily_performance': json.dumps(daily_performance),
    }
    return render(request, 'portal/dashboard.html', context)


@login_required
def material_issue(request):
    if request.method == 'POST':
        MaterialIssue.objects.create(
            date=request.POST.get('date'),
            person=request.POST.get('person'),
            material_category=request.POST.get('material_category', ''),
            material_description=request.POST.get('material_description', ''),
            material_size=request.POST.get('material_size', ''),
            unit=request.POST.get('unit', ''),
            issued_quantity=request.POST.get('issued_quantity') or 0,
            site_name=request.POST.get('site_name', ''),
            remarks=request.POST.get('remarks', ''),
        )
        return redirect('material_issue')
    return render(request, 'portal/material_issue.html')


@login_required
def material_consume(request):
    if request.method == 'POST':
        installed_quantity = float(request.POST.get('installed_quantity') or 0)
        issued_quantity = float(request.POST.get('issued_quantity') or 0)
        remaining_quantity = float(request.POST.get('remaining_quantity') or (issued_quantity - installed_quantity))
        MaterialConsumption.objects.create(
            date=request.POST.get('date'),
            person=request.POST.get('person'),
            site_name=request.POST.get('site_name', ''),
            material_description=request.POST.get('material_description', ''),
            material_size=request.POST.get('material_size', ''),
            issued_quantity=issued_quantity,
            installed_quantity=installed_quantity,
            remaining_quantity=remaining_quantity,
            remarks=request.POST.get('remarks', ''),
        )
        return redirect('material_consume')
    return render(request, 'portal/material_consume.html')


@login_required
def dpr(request):
    if request.method == 'POST':
        DPR.objects.create(
            date=request.POST.get('date'),
            person=request.POST.get('person'),
            rfc_quantity=request.POST.get('rfc_quantity') or 0,
            ng_quantity=request.POST.get('ng_quantity') or 0,
            tf_quantity=request.POST.get('tf_quantity') or 0,
            gi_quantity=request.POST.get('gi_quantity') or 0,
            remarks=request.POST.get('remarks', ''),
        )
        return redirect('dpr')
    return render(request, 'portal/dpr.html')


@login_required
def expenses(request):
    if request.method == 'POST':
        Expense.objects.create(
            date=request.POST.get('date'),
            person=request.POST.get('person'),
            category=request.POST.get('category', ''),
            description=request.POST.get('description', ''),
            amount=request.POST.get('amount') or 0,
            site_name=request.POST.get('site_name', ''),
            reference=request.POST.get('reference', ''),
            remarks=request.POST.get('remarks', ''),
        )
        return redirect('expenses')
    return render(request, 'portal/expenses.html')


@login_required
def reports(request):
    return render(request, 'portal/reports.html')


@login_required
def export_excel(request):
    wb = Workbook()
    models = [
        ('Material Issue', MaterialIssue, ['date', 'person', 'material_category', 'material_description', 'material_size', 'unit', 'issued_quantity', 'site_name', 'remarks']),
        ('Material Consumption', MaterialConsumption, ['date', 'person', 'site_name', 'material_description', 'material_size', 'issued_quantity', 'installed_quantity', 'remaining_quantity', 'remarks']),
        ('DPR', DPR, ['date', 'person', 'rfc_quantity', 'ng_quantity', 'tf_quantity', 'gi_quantity', 'remarks']),
        ('Expense', Expense, ['date', 'person', 'category', 'description', 'amount', 'site_name', 'reference', 'remarks']),
    ]
    for title, model, fields in models:
        ws = wb.create_sheet(title=title)
        ws.append(fields)
        for item in model.objects.all().values_list(*fields):
            ws.append(list(item))
    wb.remove(wb['Sheet'])
    stream = io.BytesIO()
    wb.save(stream)
    stream.seek(0)
    response = HttpResponse(stream, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=dashboard_report.xlsx'
    return response


@login_required
def export_pdf(request):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle('Dashboard Report')
    y = 750
    pdf.setFont('Helvetica-Bold', 14)
    pdf.drawString(40, y, 'Dashboard Portal Report')
    y -= 30
    pdf.setFont('Helvetica', 10)
    data = [
        ('Material Issues', MaterialIssue.objects.count()),
        ('Material Consumptions', MaterialConsumption.objects.count()),
        ('DPR Entries', DPR.objects.count()),
        ('Expense Entries', Expense.objects.count()),
    ]
    for label, count in data:
        pdf.drawString(40, y, f'{label}: {count}')
        y -= 20
    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')
