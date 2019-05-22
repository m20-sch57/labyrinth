<script type='text/javascript'>
    $('[contenteditable="plaintext-only"]').attr('contenteditable', 'true').addClass('contenteditable-plaintext-only');
    $('.contenteditable-plaintext-only').on('paste', function(e) {
        console.log('paste');
        e.preventDefault();

        if( e.originalEvent.clipboardData ) {
            var content = $.trim(e.originalEvent.clipboardData.getData('text/plain'))
            document.execCommand('insertText', false, content);
        }
    });
    $(document).ready(function() {$('.contenteditable-plaintext-only').addClass('chat-input-show-placeholder');});
    $('.contenteditable-plaintext-only').on('change paste keyup load', function() {
        if ($(this).text()) {
            $(this).removeClass('chat-input-show-placeholder');
        } else {
            $(this).addClass('chat-input-show-placeholder');
        }
    });
</script>