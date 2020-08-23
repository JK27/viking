/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment
    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

/*  Get Stripe Public Key and Client Secret from template as text,
    slicing off the quotations which are first and last characters.
*/
var stripePublicKey  = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret  = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublicKey );
var elements = stripe.elements();

// STYLE
var style = {
    base: {
        color: '#293949',
        fontFamily: '"Oswald", Oswald, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};

// CARD ELEMENT
// Creates card element and send it to field in template
var card = elements.create('card', {style: style});
card.mount('#card-element');

// HANDLE REALTIME VALIDATION ERRORS ON CARD ELEMENT
/*  Each time there is a change in the card element,
    will check for errors */
card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    /* If there is and error, it displays in card-errors div in template */
    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

// HANDLE FORM SUBMIT
var form = document.getElementById('checkout-form');

form.addEventListener('submit', function(ev) {      // When user clicks submit button...
    ev.preventDefault();                            // ... prevents form from submitting...
    card.update({ 'disabled': true});               // ... instead disables card element...
    $('#submit-button').attr('disabled', true);     // ... and button to avoid multiple submissions...
    $('#checkout-form').fadeToggle(100);            // ... hides form...
    $('#loading-overlay').fadeToggle(100);          // ... and triggers loading overlay

    /* Capture form data and post it to cache_payment_data view */
    /* From using {% csrf_token %} in the form */
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
    };
    var url = '/checkout/cache_checkout_data/';

    $.post(url, postData).done(function() {         // When view returns 200 response...
        stripe.confirmCardPayment(clientSecret, {   // ... call confirm method from Stripe
            payment_method: {
                card: card,
                billing_details: {
                    name: $.trim(form.full_name.value),
                    phone: $.trim(form.phone_number.value),
                    email: $.trim(form.email.value),
                    address:{
                        line1: $.trim(form.street_address1.value),
                        line2: $.trim(form.street_address2.value),
                        city: $.trim(form.town_or_city.value),
                        country: $.trim(form.country.value),
                        state: $.trim(form.county.value),
                    }
                }
            },
        }).then(function(result) {
            if (result.error) {                             // If there is an error in the form...
                var errorDiv = document.getElementById('card-errors');
                var html = `
                    <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                    </span>
                    <span>${result.error.message}</span>`;
                $(errorDiv).html(html);                         // ... displays error for user...
                $('#checkout-form').fadeToggle(100);
                $('#loading-overlay').fadeToggle(100);          // ... hides loading overlay...
                card.update({ 'disabled': false});              // ... re-enables card element...
                $('#submit-button').attr('disabled', false);    // ... and submit button
            } else {                                                // If everything OK...
                if (result.paymentIntent.status === 'succeeded') {  // ... submits form
                    form.submit();
                }
            }
        });
    }).fail(function () {               // If there is an error posting the data to view...
        // ... just reload the page, the error will be in django messages without charging the user
        location.reload();
    })
});