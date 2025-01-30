// Copyright 2022 Vitaly Volkov (@vlkv)
// SPDX-License-Identifier: GPL-2.0-or-later
#include "oled.h"

#define _QWERTY 0
#define _LOWER 1
#define _RAISE 2
#define _ADJUST 3
#define _UNICODE 4
#define _MY_BUTTON 5

#ifdef OLED_ENABLE
oled_rotation_t oled_init_kb(oled_rotation_t rotation) {
    return OLED_ROTATION_180;
}

void matrix_init_user(void) {
    set_unicode_input_mode(UNICODE_MODE_LINUX);
}

// bool oled_task_kb(void) {
//     if (!oled_task_user()) {
//         return false;
//     }
//     oled_write_P(PSTR("Avalanche\nVersion 4"), false);
//     return true;
// }

bool oled_task_user(void) {
    // Host Keyboard Layer Status
    // oled_write_P(PSTR("Layer: "), false);

    switch (get_highest_layer(layer_state)) {
        case _QWERTY:
            oled_write_P(PSTR("First "), false);
            break;
        case _LOWER:
            oled_write_P(PSTR("Second "), false);
            // rgb_matrix_set_color_all(0, 255, 255);

            // uint8_t last_val = rgb_matrix_get_val();
            if (!is_keyboard_master()) {
                // oled_write_P(PSTR("SLAVE\n"), false);
                // oled_write_P(const char*)last_val, false);
                // uprintf("not master int: %u\n", rgb_matrix_get_val());
            } else {
                // oled_write_P((const char*)last_val, false);
                // uprintf("master int: %u\n", rgb_matrix_get_val());
            }

            break;
        case _RAISE:
            oled_write_P(PSTR("Therd "), false);
            break;
        case _ADJUST:
            oled_write_P(PSTR("Fourht "), false);
            break;
        default:
            // Or use the write_ln shortcut over adding '\n' to the end of your string
            // oled_write_ln_P(PSTR("Undefined"), false);
    }
    switch (get_unicode_input_mode()) {
        case UNICODE_MODE_LINUX:
            oled_write_P(PSTR("Linux"), false);
            break;
        case UNICODE_MODE_MACOS:
            oled_write_P(PSTR("apple"), false);
            break;
        case UNICODE_MODE_WINDOWS:
            oled_write_P(PSTR("windows"), false);
            break;
        case UNICODE_MODE_WINCOMPOSE:
            oled_write_P(PSTR("windows c"), false);
            break;
        case UNICODE_MODE_BSD:
            oled_write_P(PSTR("bsd"), false);
            break;
        case UNICODE_MODE_EMACS:
            oled_write_P(PSTR("emacs"), false);
            break;
        default:
            oled_write_ln_P(PSTR("not supported"), false);
    }

    // Host Keyboard LED Status
    led_t led_state = host_keyboard_led_state();
    oled_write_P(led_state.num_lock ? PSTR("NUM ") : PSTR("    "), false);
    oled_write_P(led_state.caps_lock ? PSTR("CAP ") : PSTR("    "), false);
    oled_write_P(led_state.scroll_lock ? PSTR("SCR ") : PSTR("    "), false);

    oled_set_cursor(0, 2);
    oled_write_raw_P(hello_world_img, sizeof(hello_world_img));

    /* oled_set_cursor(0, 5); */
    /* oled_write_P(PSTR("-----"), false); */

    // oled_write_P(hello_world_img, false);

    return false;
}
#endif

void housekeeping_task_user(void) {
    // oled_write_ln_P(PSTR("xxxxxx"), false);
    if (!is_keyboard_master()) {
        // rgblight_setrgb_range(RGB_RED, 20, 30);
        // rgblight_setrgb_range(RGB_RED, 50, 57);
        // rgb_matrix_set_color_all(RGB_RED);
    }

    // if (!is_keyboard_master()) {
    //         uprintf("not master int: %u\n", rgb_matrix_get_val());
    //         // uprintf не работает на slave
    // } else {
    //     if (timer_elapsed(saver_timer) > 2000) {
    //         saver_timer = timer_read();
    //         uprintf("master int: %u time %u\n", rgb_matrix_get_val(), saver_timer);
    //     }
    //         //uprintf("master int: %u time %u\n", rgb_matrix_get_val(), saver_timer);
    // }
}

// void keyboard_post_init_user(void) {
//   // Customise these values to desired behaviour
//   debug_enable=true;
//   debug_matrix=true;
//   //debug_keyboard=true;
//   //debug_mouse=true;
//   oled_write_ln_P(PSTR("post_init"), false);

// }
