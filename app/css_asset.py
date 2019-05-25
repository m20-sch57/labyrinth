from flask_assets import Bundle

css_asset = Bundle(
    'css/vars.css',
    'css/buttons.css',
    'css/groom.css',
    'css/header.css',
    'css/info_block.css',
    'css/light.css',
    'css/room_block.css',
    'css/svg.css',
    'css/user_block.css',
    'css/wroom.css',
    'css/form.css',
    filters='cssmin', 
    output='assets/all-min.css'
    )