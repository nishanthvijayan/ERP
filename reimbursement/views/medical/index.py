from django.shortcuts import render, get_object_or_404
from django.http import Http404

from reimbursement.models.medical.medical import Medical


def show(request, medical_id):
    medical = get_object_or_404(Medical, id=medical_id)
    if request.user.groups.filter(name='Reimbursement_Medical_Change_State').exists() \
            or Medical.objects.filter(id=medical_id).filter(general_detail__employee__user_id=request.user.id).exists():
        context = {
            'medical': medical
        }
        return render(request, 'reimbursement/medical/index.html', context)
    else:
        raise Http404
