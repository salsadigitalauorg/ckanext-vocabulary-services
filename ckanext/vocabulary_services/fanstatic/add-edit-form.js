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
        for (var i = 0; i < options.length; i++) {
            $linkedSchemaFieldEl.append('<option value="' + options[i].value + '" data-name="' + options[i].name + '">' + options[i].text + '</option>')
        }

        $linkedSchemaFieldEl.change();
    });

    // Update name field.
    $linkedSchemaFieldEl.change(function (e) {
        console.log($(this).find('option:selected'));
        console.log($(this).find('option:selected').attr('data-name'));
        $nameEl.val($(this).find('option:selected').attr('data-name'));
    });
});
