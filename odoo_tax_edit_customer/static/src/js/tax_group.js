odoo.define('odoo_tax_edit_customer.tax_group', function (require) {
  "use strict";
  var core = require('web.core');
  var fieldRegistry = require('web.field_registry');
  var QWeb = core.qweb;
  var TaxGroup = fieldRegistry.get('tax-group-custom-field');
  TaxGroup.include({
    _render: function () {
        var self = this;
        // Display the pencil and allow the event to click and edit only on purchase that are not posted and in edit mode.
        // since the field is readonly its mode will always be readonly. Therefore we have to use a trick by checking the 
        // formRenderer (the parent) and check if it is in edit in order to know the correct mode.
        var displayEditWidget = this.record.data.state === 'draft' && this.getParent().mode === 'edit';
        this.$el.html($(QWeb.render('AccountTaxGroupTemplate', {
            lines: self.value,
            displayEditWidget: displayEditWidget,
        })));
    },
  });

});
