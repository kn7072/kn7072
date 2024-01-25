// Copyright 2023 Danny Nguyen (@nooges)
// SPDX-License-Identifier: GPL-2.0-or-later

#include QMK_KEYBOARD_H
#include "print.h"

#define _QWERTY 0
#define _LOWER 1
#define _RAISE 2
#define _ADJUST 3
#define _MY_BUTTON 4

enum custom_keycodes {
  QWERTY = SAFE_RANGE,
  LOWER,
  RAISE,
  ADJUST,
  MY_BUTTON
};

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {

  [_QWERTY] = LAYOUT(
  //┌────────┬────────┬────────┬────────┬────────┬────────┐                          ┌────────┬────────┬────────┬────────┬────────┬────────┐
     KC_ESC,  KC_1,    KC_2,    KC_3,    KC_4,    KC_5,                               KC_6,    KC_7,    KC_8,    KC_9,    KC_0,    KC_DELETE,
  //├────────┼────────┼────────┼────────┼────────┼────────┤                          ├────────┼────────┼────────┼────────┼────────┼────────┤
     KC_TAB,  KC_Q,    KC_W,    KC_E,    KC_R,    KC_T,                               KC_Y,    KC_U,    KC_I,    KC_O,    KC_P,    KC_BACKSPACE,
  //├────────┼────────┼────────┼────────┼────────┼────────┤                          ├────────┼────────┼────────┼────────┼────────┼────────┤
     KC_LSFT, KC_A,    KC_S,    KC_D,    KC_F,    KC_G,                               KC_H,    KC_J,    KC_K,    KC_L,    KC_SCLN, KC_QUOT,
  //├────────┼────────┼────────┼────────┼────────┼────────┼────────┐        ┌────────┼────────┼────────┼────────┼────────┼────────┼────────┤
     KC_LCTL, KC_Z,    KC_X,    KC_C,    KC_V,    KC_B,    MY_BUTTON,        KC_BSLS, KC_N,    KC_M,    KC_COMM, KC_DOT,  KC_SLSH, KC_RSFT,
  //└────────┴────────┴────────┴───┬────┴───┬────┴───┬────┴───┬────┘        └───┬────┴───┬────┴───┬────┴───┬────┴────────┴────────┴────────┘
                                    QK_LEADER, LOWER,   KC_SPC,                  KC_ENT,  RAISE,   KC_LALT
                                // └────────┴────────┴────────┘                 └────────┴────────┴────────┘
  ),

  [_LOWER] = LAYOUT(
  //┌────────┬────────┬────────┬────────┬────────┬────────┐                          ┌────────┬────────┬────────┬────────┬────────┬────────┐
     KC_TILD, KC_EXLM, KC_AT,   KC_HASH, KC_DLR,  KC_PERC,                            KC_CIRC, KC_AMPR, KC_ASTR, KC_LPRN, KC_RPRN, _______,
  //├────────┼────────┼────────┼────────┼────────┼────────┤                          ├────────┼────────┼────────┼────────┼────────┼────────┤
     QK_BOOT, KC_1,    KC_2,    KC_3,    KC_4,    KC_5,                               KC_6,    KC_7,    KC_8,    KC_9,    KC_0,    _______,
  //├────────┼────────┼────────┼────────┼────────┼────────┤                          ├────────┼────────┼────────┼────────┼────────┼────────┤
     KC_LSFT, KC_APP,  KC_BSLS, KC_HOME, KC_END,   KC_PSCR,                           KC_LEFT, KC_DOWN, KC_UP,   KC_RIGHT, KC_MINS, KC_EQL,
  //├────────┼────────┼────────┼────────┼────────┼────────┼────────┐        ┌────────┼────────┼────────┼────────┼────────┼────────┼────────┤
     KC_LCTL, KC_PGDN, KC_PGUP, KC_BACKSPACE, KC_DELETE,  KC_LWIN, _______,          KC_RPRN, KC_LBRC, KC_RBRC, KC_COMM, KC_DOT,  KC_SLSH, _______,
  //└────────┴────────┴────────┴───┬────┴───┬────┴───┬────┴───┬────┘        └───┬────┴───┬────┴───┬────┴───┬────┴────────┴────────┴────────┘
                                    _______, _______, KC_SPC,                    KC_ENT,  _______, _______
                                // └────────┴────────┴────────┘                 └────────┴────────┴────────┘
  ),

  [_RAISE] = LAYOUT(
  //┌────────┬────────┬────────┬────────┬────────┬────────┐                          ┌────────┬────────┬────────┬────────┬────────┬────────┐
     KC_F12,  KC_F1,   KC_F2,   KC_F3,   KC_F4,   KC_F5,                              KC_F6,   KC_F7,   KC_F8,   KC_F9,   KC_F10,  KC_F11,
  //├────────┼────────┼────────┼────────┼────────┼────────┤                          ├────────┼────────┼────────┼────────┼────────┼────────┤
     RGB_TOG, KC_EXLM, KC_AT,   KC_HASH, KC_DLR,  KC_PERC,                            KC_CIRC, KC_AMPR, KC_ASTR, KC_LPRN, KC_RPRN, _______,
  //├────────┼────────┼────────┼────────┼────────┼────────┤                          ├────────┼────────┼────────┼────────┼────────┼────────┤
     RGB_MOD, KC_MPRV, KC_MNXT, KC_VOLU, KC_PGUP, KC_UNDS,                            KC_EQL,  KC_HOME, RGB_HUI, RGB_SAI, RGB_VAI, KC_BSLS,
  //├────────┼────────┼────────┼────────┼────────┼────────┼────────┐        ┌────────┼────────┼────────┼────────┼────────┼────────┼────────┤
     KC_MUTE, KC_MSTP, KC_MPLY, KC_VOLD, KC_PGDN, KC_MINS, _______,          _______, KC_PLUS, KC_END,  RGB_HUD, RGB_SAD, RGB_VAD, _______,
  //└────────┴────────┴────────┴───┬────┴───┬────┴───┬────┴───┬────┘        └───┬────┴───┬────┴───┬────┴───┬────┴────────┴────────┴────────┘
                                    _______, _______, _______,                   _______, _______, _______
                                // └────────┴────────┴────────┘                 └────────┴────────┴────────┘
  ),

  [_ADJUST] = LAYOUT(
  //┌────────┬────────┬────────┬────────┬────────┬────────┐                          ┌────────┬────────┬────────┬────────┬────────┬────────┐
     _______, _______, _______, _______, _______, _______,                            _______, _______, _______, _______, _______, _______,
  //├────────┼────────┼────────┼────────┼────────┼────────┤                          ├────────┼────────┼────────┼────────┼────────┼────────┤
     _______, _______, _______, _______, _______, _______,                            _______, _______, _______, _______, _______, _______,
  //├────────┼────────┼────────┼────────┼────────┼────────┤                          ├────────┼────────┼────────┼────────┼────────┼────────┤
     _______, _______, _______, _______, _______, _______,                            _______, _______, _______, _______, _______, _______,
  //├────────┼────────┼────────┼────────┼────────┼────────┼────────┐        ┌────────┼────────┼────────┼────────┼────────┼────────┼────────┤
     _______, _______, _______, _______, _______, _______, _______,          _______, _______, _______, _______, _______, _______, _______,
  //└────────┴────────┴────────┴───┬────┴───┬────┴───┬────┴───┬────┘        └───┬────┴───┬────┴───┬────┴───┬────┴────────┴────────┴────────┘
                                    _______, _______, _______,                   _______, _______, _______
                                // └────────┴────────┴────────┘                 └────────┴────────┴────────┘
  )
};

uint8_t mod_state;
static bool my_button_is_held = false;


bool process_record_user(uint16_t keycode, keyrecord_t *record) {
  // static bool bspc_is_held = false;
  
  mod_state = get_mods();
  
  switch (keycode) {
    case MY_BUTTON:
      my_button_is_held = record->event.pressed;
      break;
    case KC_BACKSPACE: {
        // Initialize a boolean variable that keeps track
        // of the delete key status: registered or not?
        static bool delkey_registered;
        if (record->event.pressed) {
            // Detect the activation of either shift keys
            if (mod_state & MOD_MASK_SHIFT) {
                // First temporarily canceling both shifts so that
                // shift isn't applied to the KC_DEL keycode
                del_mods(MOD_MASK_SHIFT);
                register_code(KC_DEL);
                // Update the boolean variable to reflect the status of KC_DEL
                delkey_registered = true;
                // Reapplying modifier state so that the held shift key(s)
                // still work even after having tapped the Backspace/Delete key.
                set_mods(mod_state);
                return false;
            }
        } else { // on release of KC_BSPC
            // In case KC_DEL is still being sent even after the release of KC_BSPC
            if (delkey_registered) {
                unregister_code(KC_DEL);
                delkey_registered = false;
                return false;
            }
        }
        // Let QMK process the KC_BSPC keycode as usual outside of shift
        return true;
    }
    case QWERTY:
      if (record->event.pressed) {
        set_single_persistent_default_layer(_QWERTY);
      }
      return false;
      break;
    case LOWER:
      if (record->event.pressed) {
        layer_on(_LOWER);
        update_tri_layer(_LOWER, _RAISE, _ADJUST);
      } else {
        layer_off(_LOWER);
        update_tri_layer(_LOWER, _RAISE, _ADJUST);
      }
      return false;
      break;
    case RAISE:
      if (record->event.pressed) {
        layer_on(_RAISE);
        update_tri_layer(_LOWER, _RAISE, _ADJUST);
      } else {
        layer_off(_RAISE);
        update_tri_layer(_LOWER, _RAISE, _ADJUST);
      }
      return false;
      break;
    case ADJUST:
      if (record->event.pressed) {
        layer_on(_ADJUST);
      } else {
        layer_off(_ADJUST);
      }
      return false;
      break;

    // case KC_BSPC:
    //   bspc_is_held = record->event.pressed;
    //   break;

    // case KC_J: {  // Backspace + J = PgDn.
    //   static uint8_t registered_key = KC_NO;
    //   if (record->event.pressed) {
    //     registered_key = (bspc_is_held) ? KC_PGDN : KC_J;
    //     register_code(registered_key);
    //   } else {
    //     unregister_code(registered_key);
    //   }
    // return false;
    // } 

    // case KC_K: {  // Backspace + K = PgUp.
    //   static uint8_t registered_key = KC_NO;
    //   if (record->event.pressed) {
    //     registered_key = (bspc_is_held) ? KC_PGUP : KC_K;
    //     register_code(registered_key);
    //   } else {
    //     unregister_code(registered_key);
    //   }
    // return false;
    // }

    case KC_A: {  // 
      static uint8_t registered_key = KC_NO;
      if (record->event.pressed) {
        registered_key = (my_button_is_held) ? KC_CAPS_LOCK : KC_A;
        register_code(registered_key);
      } else {
        unregister_code(registered_key);
      }
    return false;
    }

    // case KC_ ... KC_L: {//  https://docs.qmk.fm/#/ChangeLog/20231126?id=switch-statement-helpers-for-keycode-ranges
    default: {  // MY_BUTTON + J = PgDn.
      if (record->event.pressed) {
        if (my_button_is_held) {
          uint8_t row = record->event.key.row;
          uint8_t col = record->event.key.col;
          // send_word(row);
          // send_word(col);
          if (row == 7 ) {
            // send_word(row);
            switch (col) {
                case 5:
                    // h
                    // send_word(col);
                    layer_move(_QWERTY);
                    break;
                case 4:
                    // j
                    // send_word(col);
                    layer_move(_LOWER);
                    break;
                case 3:
                    // k
                    // send_word(col);
                    layer_move(_RAISE);
                    break;
                case 2:
                    // l
                    // send_word(col);
                    layer_move(_ADJUST);
                    break;
            }
          }
          return false;
        }
      }  
    }
  }  
  return true;
};


const uint16_t PROGMEM test_combo1[] = {KC_A, KC_B, COMBO_END};
const uint16_t PROGMEM test_combo2[] = {KC_C, KC_D, COMBO_END};
combo_t key_combos[] = {
    COMBO(test_combo1, KC_ESC),
    COMBO(test_combo2, LCTL(KC_Z)), // keycodes with modifiers are possible too!
};

void leader_end_user(void) {
    if (leader_sequence_one_key(KC_F)) {
        // Leader, f => Types the below string
        SEND_STRING("QMK is awesome.");
    } else if (leader_sequence_two_keys(KC_D, KC_D)) {
        // Leader, d, d => Ctrl+A, Ctrl+C
        SEND_STRING(SS_LCTL("a") SS_LCTL("c"));
    } else if (leader_sequence_three_keys(KC_D, KC_D, KC_S)) {
        // Leader, d, d, s => Types the below string
        SEND_STRING("https://start.duckduckgo.com\n");
    } else if (leader_sequence_two_keys(KC_A, KC_S)) {
        // Leader, a, s => GUI+S
        tap_code16(LGUI(KC_S));
    } else if (leader_sequence_one_key(KC_T)) {
        // Leader, Left Control, Left Alt, t => open terminal
        tap_code16(LCA(KC_T));  // Hold Left Control and Alt and press kc
    } else if (leader_sequence_one_key(KC_H) || leader_sequence_one_key(KC_LEFT)) {
         // layer_on(_QWERTY);
         layer_move(_QWERTY);
    } else if (leader_sequence_one_key(KC_E)) { //|| leader_sequence_one_key(KC_DOWN)
         // layer_on(_LOWER);
         SEND_STRING("xxx");
         layer_move(_LOWER);
    } else if (leader_sequence_one_key(KC_K) || leader_sequence_one_key(KC_UP)) {
         // layer_on(_RAISE);
         layer_move(_RAISE);
    } else if (leader_sequence_one_key(KC_L) || leader_sequence_one_key(KC_RIGHT)) {
         layer_move(_ADJUST);
    } else if (leader_sequence_one_key(KC_RALT)) {
        layer_move(_QWERTY);
        //layer_on(_QWERTY);
    }  else if (leader_sequence_one_key(KC_Q)) {
        SEND_STRING("qqqqqq");
        //layer_on(_QWERTY);
    }
// else if (leader_sequence_one_key(QK_LEADER)) {
//         layer_on(_QWERTY);
//    }
};

layer_state_t layer_state_set_user(layer_state_t state) {
    switch (get_highest_layer(state)) {
    case _RAISE:
        rgblight_setrgb (0x00,  0x00, 0xFF);
        break;
    case _LOWER:
        rgblight_setrgb (0xFF,  0x00, 0x00);
        break;
    case _QWERTY:
        rgblight_setrgb (0x00,  0xFF, 0x00);
        break;
    case _ADJUST:
        rgblight_setrgb (0x7A,  0x00, 0xFF);
        break;
    default: //  for any other layers, or the default layer
        rgblight_setrgb (0x00,  0xFF, 0xFF);
        break;
    }
  return state;
};
