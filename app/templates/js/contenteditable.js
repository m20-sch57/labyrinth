<script type='text/javascript'>
    $('[contenteditable="plaintext-only"]').attr('contenteditable', 'true').addClass('contenteditable-plaintext-only')
    $('.contenteditable-plaintext-only').on('paste', function(e) {
         e.preventDefault();
         
         if( e.originalEvent.clipboardData ) {
              var content = e.originalEvent.clipboardData.getData('text/plain').replace(/\r\n|\r|\n/g, '');
              console.log('pasted content only text', content);
              document.execCommand('insertText', false, content);
        }
    });
</script>