// Copyright 2022 Will Winder (@winder)
// SPDX-License-Identifier: GPL-2.0-or-later

#pragma once

// #define RGBLIGHT_DEFAULT_MODE RGBLIGHT_MODE_RAINBOW_SWIRL

#define MASTER_LEFT

#ifdef OLED_ENABLE
#define OLED_DISPLAY_128X64
#define OLED_TIMEOUT 30000
#endif

#define RP2040_BOOTLOADER_DOUBLE_TAP_RESET
#define RP2040_BOOTLOADER_DOUBLE_TAP_RESET_LED GP17
#define RP2040_BOOTLOADER_DOUBLE_TAP_RESET_TIMEOUT 1000U

/* key combination for command */
#define IS_COMMAND() ( \
    get_mods() == (MOD_BIT(KC_LCTL) | MOD_BIT(KC_LSFT) )|| \
    get_mods() == (MOD_BIT(KC_LSFT) | MOD_BIT(KC_RSFT) | MOD_BIT(KC_RALT))\
)
#define MAGIC_KEY_EEPROM_CLEAR A

// https://github.com/joric/qmk/blob/master/docs/feature_bootmagic.md
#define BOOTMAGIC_LITE_ROW 0
#define BOOTMAGIC_LITE_COLUMN 0

//  The firmware is too large!
#define COMBO_TERM 300 // timeout period for combos to 40ms.

#define LEADER_TIMEOUT 500
#define QUICK_TAP_TERM 300
#define TAPPING_TERM 300

#ifdef RGBLIGHT_ENABLE
#define RGBLIGHT_LAYERS
#define RGBLIGHT_DEFAULT_MODE RGBLIGHT_MODE_RAINBOW_SWIRL+2
#endif


// https://docs.qmk.fm/#/feature_split_keyboard?id=data-sync-options
#define SPLIT_LED_STATE_ENABLE
// #define SPLIT_MODS_ENABLE
#define SPLIT_LAYER_STATE_ENABLE
#define RGBLED_SPLIT { 32, 32 }

#define VIAL_KEYBOARD_UID {0x58, 0x8C, 0xA2, 0x28, 0x65, 0xFA, 0xE1, 0x58}
#define VIAL_UNLOCK_COMBO_ROWS { 2, 2 }
#define VIAL_UNLOCK_COMBO_COLS { 1, 4 }
