/**
 * Created by Jainendra Mandavi on 06-05-2017.
 */
$(function () {
    $('.consultation-formset').formset({
        prefix:'consultation_formset',
        addText: 'Add another',
        deleteText: ''
    });
    $('.injection-formset').formset({
        prefix:'injection_formset',
        addText: 'Add another',
        deleteText: ''
    });
    $('.specialist-consultation-formset').formset({
        prefix:'specialist_consultation_formset',
        addText: 'Add another',
        deleteText: ''
    });
    $('.medicine-formset').formset({
        prefix:'medicine_formset',
        addText: 'Add another',
        deleteText: ''
    });
    $('.medical-bill-formset').formset({
        prefix:'medical_bill_formset',
        addText: 'Add another',
        deleteText: ''
    });
    $('.add-row').addClass('btn btn-primary btn-xs pull-right')
});
