#include QMK_KEYBOARD_H
#include "../../common_functions.c"
#include "../../my_unicode.h"
#include "../../rgb.c"

#define A_LGUI LGUI_T(KC_A)
#define KC_APP_LGUI LGUI_T(KC_APP)
#define S_LALT LALT_T(KC_S)
#define D_LSFT LSFT_T(KC_D)
#define F_LCTL LCTL_T(KC_F)
#define J_RCTL RCTL_T(KC_J)
#define K_RSFT RSFT_T(KC_K)
#define L_LALT LALT_T(KC_L)
#define SCLN_RGUI RGUI_T(KC_SCLN)
#define BSLS_LALT LALT_T(KC_BSLS)
#define HOME_LSFT LSFT_T(KC_HOME)
#define END_LCTL LCTL_T(KC_END)
#define Q_LCTL LCTL_T(KC_Q)
#define DOWN_RCTL RCTL_T(KC_DOWN)
#define UP_RSFT RSFT_T(KC_UP)
#define RIGHT_LALT LALT_T(KC_RIGHT)
#define MINS_RGUI RGUI_T(KC_MINS)
#define LSFT_DEL RSFT(KC_DEL)

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {

    [_QWERTY] = LAYOUT(
        KC_GRAVE, KC_1, KC_2, KC_3, KC_4, KC_5, KC_6, KC_7, KC_8, KC_9, KC_0, KC_DELETE, KC_LSFT, KC_Q, KC_W, KC_E,
        KC_R, KC_T, KC_Y, KC_U, KC_I, KC_O, KC_P, KC_LBRC, KC_ESC, KC_TAB, A_LGUI, S_LALT, D_LSFT, F_LCTL, KC_G, KC_H,
        J_RCTL, K_RSFT, L_LALT, SCLN_RGUI, KC_QUOT, KC_CAPS_LOCK, KC_LCTL, KC_Z, KC_X, KC_C, KC_V, KC_B, QK_LEADER,
        KC_HOME, KC_END, KC_BSLS, KC_N, KC_M, KC_COMM, KC_DOT, KC_SLSH, KC_RBRC, KC_LWIN, MY_BUTTON, KC_SPC, LOWER,
        KC_DELETE, KC_BACKSPACE, RAISE, KC_ENT, TG(_UNICODE), KC_PSCR),

    [_LOWER] = LAYOUT(
        _______, _______, _______, KC_MUTE, KC_MEDIA_STOP, KC_MPLY, KC_LEFT, KC_DOWN, KC_UP, KC_RIGHT, Q_LCTL, LSFT_DEL,
        _______, KC_1, KC_2, KC_3, KC_4, KC_5, KC_6, KC_7, KC_8, KC_9, KC_0, KC_LBRC, _______, _______, KC_APP_LGUI,
        BSLS_LALT, HOME_LSFT, END_LCTL, KC_LPRN, KC_LEFT, DOWN_RCTL, UP_RSFT, RIGHT_LALT, MINS_RGUI, KC_EQL,
        KC_CAPS_LOCK, _______, KC_PGDN, KC_PGUP, KC_BACKSPACE, KC_DELETE, KC_RPRN, _______, _______, _______, KC_PSCR,
        KC_LBRC, KC_RBRC, KC_COMM, KC_DOT, KC_SLSH, _______, _______, _______, _______, _______, _______, _______,
        _______, _______, _______, _______),

    [_RAISE] = LAYOUT(
        KC_F12, KC_F1, KC_F2, KC_F3, KC_F4, KC_F5, KC_F6, KC_F7, KC_F8, KC_F9, KC_F10, KC_F11, _______, KC_EXLM, KC_AT,
        KC_HASH, KC_DLR, KC_PERC, KC_CIRC, KC_AMPR, KC_ASTR, KC_LPRN, KC_RPRN, _______, _______, _______, KC_MPRV,
        KC_MNXT, KC_VOLU, KC_PGUP, KC_MINS, KC_PLUS, KC_HOME, _______, _______, _______, KC_BSLS, _______, KC_MUTE,
        KC_MSTP, KC_MPLY, KC_VOLD, KC_PGDN, KC_UNDS, _______, _______, _______, _______, KC_EQL, KC_END, _______,
        _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______, _______,
        _______),

    [_ADJUST] = LAYOUT(

        KC_NO, KC_NO, KC_NO, KC_NO, KC_NO, KC_NO, KC_NO, KC_NO, KC_NO, KC_NO, KC_NO, KC_NO, _______, QK_BOOT, KC_NO,
        KC_NO, KC_NO, KC_NO, KC_NO, KC_NO, KC_NO, KC_NO, KC_NO, KC_NO, RGB_TOG, RGB_M_P, RGB_MOD, _______, RGB_SAI,
        RGB_HUI, RGB_VAI, KC_NO, KC_NO, KC_NO, KC_NO, KC_NO, KC_NO, _______, KC_NO, KC_NO, KC_NO, RGB_SAD, RGB_HUD,
        RGB_VAD, _______, _______, _______, _______, KC_NO, KC_NO, KC_NO, KC_NO, KC_NO, KC_NO, _______, _______,
        _______, _______, _______, _______, _______, _______, _______, _______),

    [_UNICODE] = LAYOUT(
        // UP(SE_ARNG_LOW, SE_ARNG_HIGH), UP(SE_ARNG_LOW, SE_ARNG_HIGH), UP(SE_ARNG_LOW, SE_ARNG_HIGH),
        UP(SNEK, SPEAKER_TG), UM(SQUARE), UM(zeta), UC(KING_B), KC_NO, KC_NO, KC_NO, KC_NO, KC_NO, KC_NO, KC_NO, KC_NO,
        _______, QK_BOOT, KC_NO, KC_NO, KC_NO, KC_NO, KC_NO, KC_NO, KC_NO, KC_NO, KC_NO, KC_NO, RGB_TOG, RGB_M_P,
        RGB_MOD, _______, RGB_SAI, RGB_HUI, RGB_VAI, KC_NO, KC_NO, KC_NO, KC_NO, KC_NO, KC_NO, _______, KC_NO, KC_NO,
        KC_NO, RGB_SAD, RGB_HUD, RGB_VAD, _______, _______, _______, _______, KC_NO, KC_NO, KC_NO, KC_NO, KC_NO, KC_NO,
        _______, _______, _______, _______, _______, _______, _______, _______, _______, _______)};
