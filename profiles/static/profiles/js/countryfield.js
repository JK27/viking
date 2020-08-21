let countrySelected = $('#id_profile_country').val();
// If country value is not selected...
if(!countrySelected) {
    // ... it's colour grey
    $('#id_profile_country').css('color', '#aab7c4');
};
// If country value changes...
$('#id_profile_country').change(function() {
    countrySelected = $(this).val();
    // ... if country value is not selected...
    if(!countrySelected) {
        // ... it's colour grey...
        $(this).css('color', '#aab7c4');
        // ...if county value is selected...
    } else {
        // ... it's colour black
        $(this).css('color', '#293949');
    }
});