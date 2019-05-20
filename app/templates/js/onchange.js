<script type="text/javascript">
    $(document).ready(function() {
        $('.changeble').attr('data-saved-value', function() {return $(this).val()});
        $($('.changeble').attr('data-hide-on-change')).attr('data-saved-display', function(){return $(this).css('display')});
        $($('.changeble').attr('data-show-on-change')).attr('data-saved-display', function(){return $(this).css('display')});
        $($('.changeble').attr('data-show-on-change')).css('display', 'none')
    })
    $('.changeble').on("change paste keyup", function(){
        savedValue = $(this).attr('data-saved-value')
        if (savedValue != $(this).val()) {
            $($(this).attr('data-show-on-change')).css('display', function() {return $(this).attr('data-saved-display')});
            $($(this).attr('data-hide-on-change')).css('display', 'none');
        } else {
            $($(this).attr('data-show-on-change')).css('display', 'none');
            $($(this).attr('data-hide-on-change')).css('display', function() {return $(this).attr('data-saved-display')});
        }
    })
</script>