#include QMK_KEYBOARD_H
#define _QWERTY 0
#define _LOWER 1
#define _RAISE 2
#define _ADJUST 3
#define _UNICODE 4
#define _MY_BUTTON 5

#ifdef RGBLIGHT_ENABLE
// // Light LEDs 9 & 10 in cyan when keyboard layer 1 is active
const rgblight_segment_t PROGMEM my_base_layer[] = RGBLIGHT_LAYER_SEGMENTS({0, 64, HSV_YELLOW});
// Light LEDs 11 & 12 in purple when keyboard layer 2 is active
const rgblight_segment_t PROGMEM my_lower_layer[] = RGBLIGHT_LAYER_SEGMENTS({0, 64, HSV_RED});  // HSV_WHITE
// Light LEDs 13 & 14 in green when keyboard layer 3 is active
const rgblight_segment_t PROGMEM my_raise_layer[] = RGBLIGHT_LAYER_SEGMENTS(
    // {13, 2, HSV_GREEN}
    {0, 64, HSV_GREEN});
const rgblight_segment_t PROGMEM my_adjust_layer[] = RGBLIGHT_LAYER_SEGMENTS({0, 64, HSV_BLUE});
// Light LEDs 6 to 9 and 12 to 15 red when caps lock is active. Hard to ignore!
const rgblight_segment_t PROGMEM my_caps_layer[] = RGBLIGHT_LAYER_SEGMENTS(
    {0, 25, HSV_YELLOW},  // Light 4 LEDs, starting with LED 6
    {40, 25, HSV_YELLOW}  // Light 4 LEDs, starting with LED 12
);

// Now define the array of layers. Later layers take precedence
const rgblight_segment_t *const PROGMEM my_rgb_layers[] =
    RGBLIGHT_LAYERS_LIST(my_base_layer, my_lower_layer, my_raise_layer, my_adjust_layer);  // , my_caps_layer

// void keyboard_post_init_user(void) {
//     // Enable the LED layers
//     rgblight_layers = my_rgb_layers;
// }

void keyboard_post_init_user(void) {
    // Customise these values to desired behaviour
    debug_enable = true;
    debug_matrix = true;
    // debug_keyboard=true;
    // debug_mouse=true;
    // oled_write_ln_P(PSTR("post_init"), false);

    // Enable the LED layers
    rgblight_layers = my_rgb_layers;
}

// Enabling and disabling lighting layers for default layer
layer_state_t default_layer_state_set_user(layer_state_t state) {
    rgblight_set_layer_state(0, layer_state_cmp(state, _QWERTY));
    return state;
}

layer_state_t layer_state_set_user(layer_state_t state) {
    // oled_write_ln_P(PSTR("post_init"), false);
    /* switch (get_highest_layer(state)) { */
    /*     case _RAISE: */
    /*         rgblight_setrgb(RGB_GREEN); */
    /*         // rgblight_set_layer_state(2, layer_state_cmp(state, _RAISE)); */
    /*         oled_write_ln_P(PSTR("raise\n"), false); */
    /*  */
    /*         break; */
    /*     case _LOWER: */
    /*         // rgblight_setrgb(RGB_BLUE); */
    /*         rgblight_setrgb_range(RGB_RED, 13, 15); */
    /*  */
    /*         // rgblight_set_layer_state(1, layer_state_cmp(state, _LOWER)); */
    /*         if (debug_enable) { */
    /*             rgblight_setrgb_range(RGB_TURQUOISE, 0, 1); */
    /*         } */
    /*         oled_write_ln_P(PSTR("lower\n"), false); */
    /*  */
    /*         break; */
    /*     case _QWERTY: */
    /*         rgblight_setrgb(RGB_WHITE); */
    /*         rgblight_setrgb_range(RGB_BLUE, 12, 15); */
    /*         // if (!is_keyboard_master()) { */
    /*         //         rgblight_setrgb_range(RGB_RED, 50, 60); */
    /*         // } */
    /*         // rgblight_set_layer_state(0, layer_state_cmp(state, _QWERTY)); */
    /*         break; */
    /*     case _ADJUST: */
    /*         // rgblight_setrgb (0x7A,  0x00, 0xFF); */
    /*         rgblight_setrgb_range(RGB_RED, 50, 57); */
    /*         rgblight_sethsv_range(RGB_RED, 50, 57); */
    /*         rgblight_setrgb_at(RGB_RED, 50); */
    /*         rgblight_setrgb_at(RGB_RED, 51); */
    /*         // rgblight_setrgb_slave(0x7A, 0x00, 0xFF); */
    /*         sethsv(HSV_RED, (rgb_led_t *)&led[51]);  // led 51 */
    /*         if (!is_keyboard_master()) { */
    /*             rgblight_setrgb_range(RGB_RED, 20, 30); */
    /*         } */
    /*         if (is_keyboard_left()) { */
    /*             rgblight_setrgb_range(RGB_BLUE, 10, 15); */
    /*         } */
    /*  */
    /*         // if (is_keyboard_master()) { */
    /*         //         rgblight_setrgb_range(RGB_MAGENTA, 0, 1); */
    /*         // } */
    /*         // rgblight_set_layer_state(3, layer_state_cmp(state, _ADJUST)); */
    /*  */
    /*         break; */
    /*     default:  //  for any other layers, or the default layer */
    /*         // rgblight_setrgb (0x00,  0xFF, 0xFF); */
    /*         break; */
    /* } */
    rgblight_set_layer_state(0, layer_state_cmp(state, _QWERTY));
    rgblight_set_layer_state(1, layer_state_cmp(state, _LOWER));
    rgblight_set_layer_state(2, layer_state_cmp(state, _RAISE));
    rgblight_set_layer_state(3, layer_state_cmp(state, _ADJUST));

    return state;
};

bool led_update_user(led_t led_state) {
    if (led_state.caps_lock) {
        rgblight_disable();
        rgblight_mode(RGBLIGHT_MODE_BREATHING + 3);  // RGBLIGHT_MODE_KNIGHT RGBLIGHT_EFFECT_BREATHING
        // rgblight_set_layer_state(0, led_state.caps_lock);
    } else {
        rgblight_enable();
        rgblight_mode(RGBLIGHT_MODE_STATIC_LIGHT);
    }
    return true;
};

#endif

#ifdef RGB_MATRIX_ENABLE
led_config_t g_led_config = {
    {// Key Matrix to LED Index
     // Left Half
     {27, 26, 18, 17, 8, 7, NO_LED},
     {28, 25, 19, 16, 9, 6, NO_LED},
     {29, 24, 20, 15, 10, 5, 2},
     {30, 23, 21, 14, 11, 4, 3},
     {31, NO_LED, 22, 13, 12, 0, 1},
     // Right Half
     {NO_LED, 39, 40, 49, 50, 55, 59},
     {NO_LED, 38, 41, 48, 51, 56, 60},
     {34, 37, 42, 47, 52, 57, 61},
     {35, 36, 43, 46, 53, 58, 62},
     {33, 32, 44, 45, 54, NO_LED, 63}},
    {// LED Index to Physical Position
     // Left Half
     {13, 61},
     {25, 61},
     {40, 63},
     {53, 64},
     {64, 62},
     {78, 59},
     {13, 48},
     {25, 48},
     {39, 50},
     {51, 51},
     {64, 49},
     {76, 47},
     {0, 32},
     {13, 35},
     {25, 35},
     {39, 37},
     {51, 38},
     {64, 36},
     {76, 34},
     {13, 22},
     {25, 22},
     {38, 24},
     {51, 26},
     {63, 24},
     {76, 22},
     {87, 15},
     {101, 8},
     {42, 16},
     {56, 18},
     {70, 8},
     {84, 9},
     {96, 0},
     // Right Half
     {212, 61},
     {200, 61},
     {185, 63},
     {172, 64},
     {160, 62},
     {147, 59},
     {210, 48},
     {198, 48},
     {184, 50},
     {171, 51},
     {158, 49},
     {146, 47},
     {223, 32},
     {211, 35},
     {198, 35},
     {185, 37},
     {172, 38},
     {159, 36},
     {147, 34},
     {211, 22},
     {199, 22},
     {186, 24},
     {173, 26},
     {161, 24},
     {148, 22},
     {137, 15},
     {123, 8},
     {181, 16},
     {167, 18},
     {153, 8},
     {139, 9},
     {127, 0}},
    {
     // LED Index to Flag
        // Left Half
        4, 4,
     4, 4,
     4, 4,
     4, 4,
     4, 4,
     4, 4,
     4, 4,
     4, 4,
     4, 4,
     4, 4,
     4, 4,
     4, 4,
     4, 4,
     4, 4,
     4, 4,
     4, 4,

     // Right Half
        4, 4,
     4, 4,
     4, 4,
     4, 4,
     4, 4,
     4, 4,
     4, 4,
     4, 4,
     4, 4,
     4, 4,
     4, 4,
     4, 4,
     4, 4,
     4, 4,
     4, 4,
     4, 4,

     }
};

// https://docs.qmk.fm/#/feature_rgb_matrix?id=indicator-examples-1
bool rgb_matrix_indicators_advanced_user(uint8_t led_min, uint8_t led_max) {
    if (host_keyboard_led_state().caps_lock) {
        // RGB_MATRIX_INDICATOR_SET_COLOR(32, RGB_RED); // assuming caps lock is at led #5
        rgb_matrix_set_color(1, RGB_BLUE);
    } else {
        RGB_MATRIX_INDICATOR_SET_COLOR(1, 0, 0, 0);
    }

    for (uint8_t i = led_min; i < led_max; i++) {
        switch (get_highest_layer(layer_state)) {
            case 0:
                rgb_matrix_set_color(i, RGB_BLUE);
                break;
            case 1:
                rgb_matrix_set_color(i, RGB_YELLOW);
                break;
            case 2:
                rgb_matrix_set_color(i, RGB_CORAL);
                break;
            case 3:
                rgb_matrix_set_color(i, RGB_SPRINGGREEN);
                break;
            default:
                break;
        }
    }

    // switch(get_highest_layer(layer_state)) {
    //     case 0:
    //         rgb_matrix_set_color_all(RGB_BLUE);
    //         break;
    //     case 1:
    //         rgb_matrix_set_color_all(RGB_YELLOW);
    //         break;
    //     case 2:
    //         rgb_matrix_set_color_all(RGB_CORAL);
    //         break;
    //     case 3:
    //         rgb_matrix_set_color_all(RGB_SPRINGGREEN);
    //         break;
    //     default:
    //         break;
    // }

    return false;
}

// bool rgb_matrix_indicators_advanced_user(uint8_t led_min, uint8_t led_max) {
//     if (host_keyboard_led_state().caps_lock) {
//         for (uint8_t i = led_min; i < led_max; i++) {
//             if (g_led_config.flags[i] & LED_FLAG_KEYLIGHT) {
//                 rgb_matrix_set_color(i, RGB_RED);
//             }
//         }
//     }
//     return false;
// }

#endif
