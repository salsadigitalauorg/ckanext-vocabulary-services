jQuery(document).ready(function () {
    var $vocabFormEl = jQuery('#dataset-edit');
    var $nameEl = $vocabFormEl.find('#field-name');
    var $linkedSchemaFieldEl = $vocabFormEl.find('#linked_schema_field');

    // Name field should be readonly.
    $nameEl.attr('readonly', 'readonly');

    // Update the linked schema field options.
    $vocabFormEl.find('#schema').change(function (e) {
        var options = linked_schema_field[$(this).val()];
        $linkedSchemaFieldEl.html('');
        if (options && options.length > 0) {
            for (var i = 0; i < options.length; i++) {
                var selected = '';
                if (linked_schema_field_data === options[i].value && schema_data === $(this).val()) {
                    selected = 'selected';
                    // Reset schema data. The case when user is moving the selection to other dataset
                    // and back to this dataset, the selection should be not default to the edit value.
                    schema_data = '';
                }
                $linkedSchemaFieldEl.append('<option value="' + options[i].value + '" data-name="' + options[i].name + '" ' + selected +'>' + options[i].text + '</option>')
            }
        }

        $linkedSchemaFieldEl.change();
    });

    // Update name field.
    $linkedSchemaFieldEl.change(function (e) {
        $nameEl.val($(this).find('option:selected').attr('data-name'));
    });

    // Enable select2.
    $vocabFormEl.find('#schema').change();
    $linkedSchemaFieldEl.select2();
});
