#pragma once

#ifdef VIA_ENABLE
/* VIA configuration. */
#    define DYNAMIC_KEYMAP_LAYER_COUNT 4
#endif // VIA_ENABLE

// #define FORCE_NKRO
#define COMBO_COUNT 10

//  The firmware is too large!
#define COMBO_TERM 80 // timeout period for combos to 40ms.

#define LEADER_TIMEOUT 1000

/* Disable unused features. */
/* #define NO_ACTION_ONESHOT  */

#define QUICK_TAP_TERM 150
#define TAPPING_TERM 150
