/**
 * Created by Jainendra Mandavi on 07-05-2017.
 */
$(function () {
    $('.bill-detail-formset').formset({
        prefix:'bill-detail-formset',
        addText:'Add Another',
        deleteText:''
    });
    $('.bill-image-formset').formset({
        prefix:'bill-image-formset',
        addText:'Add Another',
        deleteText:''
    });
    $('.add-row').addClass('btn btn-primary pull-right');
});
