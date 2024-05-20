#include QMK_KEYBOARD_H
//#include "debug.c"
#define _QWERTY 0
#define _LOWER 1
#define _RAISE 2
#define _ADJUST 3
#define _MY_BUTTON 4

#include "print.h"

// void matrix_positon(uint_16_t keycode, keyrecord_t *record) {
// #ifdef CONSOLE_ENABLE
//     uprintf("KL: kc: 0x%04X, col: %2u, row: %2u, pressed: %u, time: %5u, int: %u, count: %u\n", keycode, record->event.key.col, record->event.key.row, record->event.pressed, record->event.time, record->tap.interrupted, record->tap.count);
// #endif
// }

enum custom_keycodes {
  QWERTY = SAFE_RANGE,
  LOWER,
  RAISE,
  ADJUST,
  MY_BUTTON
};

uint8_t mod_state;
static bool my_button_is_held = false;

void f(uint16_t keycode) {
  switch (keycode) {
    case KC_1:
      tap_code16(KC_F1);
      break;
    case KC_2:
      tap_code16(KC_F2);
      break;
    case KC_3:
      tap_code16(KC_F3);
      break;
    case KC_4:
      tap_code16(KC_F4);
      break;
    case KC_5:
      tap_code16(KC_F5);
      break;
    case KC_6:
      tap_code16(KC_A);
      break;  
    case KC_7:
      tap_code16(KC_F7);
      break;
    case KC_8:
      tap_code16(KC_F8);
      break;
    case KC_9:
      tap_code16(KC_F9);
      break;
    case KC_0:
      tap_code16(KC_F10);
      break;
    case KC_LBRC:
      tap_code16(KC_F11);
      break;
    case KC_TAB:
      tap_code16(KC_F12);
      break;
  }
}

// 
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
    case KC_1 ... KC_0:
    case KC_TAB:
    case KC_LBRC: 
    // case KC_6 : 
    {
      if (record->event.pressed ) {
          if (mod_state & MOD_MASK_CTRL) {
            // tap_code16(KC_F5);
            // SEND_STRING("_____");
            del_mods(mod_state);
            f(keycode);
            set_mods(mod_state);
            return false;
        }
      }
      break;
    }
    case KC_B : {  // 
      static uint8_t registered_key = KC_NO;
      if (record->event.pressed) {
        registered_key = (my_button_is_held) ? KC_CAPS_LOCK : KC_B;
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
          switch(row) {
            // send_word(row);
            case 2:
              switch (col) {
                case 4: {
                  // y
                  // смена раскладки
                  register_code(KC_LEFT_ALT);
                  tap_code16(KC_LEFT_SHIFT);
                  unregister_code(KC_LEFT_ALT);
                  break;
                }
              }
              break;
            case 7:
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
                      // rgb_matrix_set_color_all(0, 255, 255);
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
  // matrix_positon(keycode, record);

  #ifdef CONSOLE_ENABLE
    // uprintf("KL: kc: 0x%04X, col: %2u, row: %2u, pressed: %u, time: %5u, int: %u, count: %u\n", keycode, record->event.key.col, record->event.key.row, record->event.pressed, record->event.time, record->tap.interrupted, record->tap.count);
  #endif
  
  return true;
};


const uint16_t PROGMEM test_combo1[] = {KC_J, KC_F, COMBO_END};
const uint16_t PROGMEM test_combo2[] = {KC_C, KC_D, COMBO_END};
combo_t key_combos[] = {
    COMBO(test_combo1, KC_1), // KC_ESC
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
    } else if (leader_sequence_one_key(KC_Q)) {
        SEND_STRING("TEST  2");
    } else if (leader_sequence_one_key(KC_V)) {
       // смена раскладки
        register_code(KC_LEFT_ALT);
        tap_code16(KC_LEFT_SHIFT);
        unregister_code(KC_LEFT_ALT);
    }
};

bool encoder_update_user(uint8_t index, bool clockwise) {
  /* With an if statement we can check which encoder was turned. */
  if (index == 0) { /* First encoder */
    /* And with another if statement we can check the direction. */
    if (clockwise) {
      /* This is where the actual magic happens: this bit of code taps on the
         Page Down key. You can do anything QMK allows you to do here.
         You'll want to replace these lines with the things you want your
         encoders to do. */
      tap_code(KC_PGDN);
    } else {
      /* And likewise for the other direction, this time Page Down is pressed. */
      tap_code(KC_PGUP);
    }
  /* You can copy the code and change the index for every encoder you have. Most
     keyboards will only have two, so this piece of code will suffice. */
  } else if (index == 1) { /* Second encoder */
    if (clockwise) {
      tap_code(KC_UP);
    } else {
      tap_code(KC_DOWN);
    }
  }
  return false;
}