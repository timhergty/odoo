odoo.define('wt_hospital.SampleHospital', function(require) {
    "use strict";

    console.log('hospital.js Loaded')
    var FormController = require('web.formController');

    var ExtendFormController = FormController.include({
        saveRecord: function(){
            console.log('saveRecord')
            var res = this.super.apply(this, arguments);
            this.do_notify('Success', 'Record Saved');
            return res;
        }
    });
});