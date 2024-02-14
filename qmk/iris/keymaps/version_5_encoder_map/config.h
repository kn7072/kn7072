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
#define QUICK_TAP_TERM 500
#define TAPPING_TERM 500

// #define NUMBER_OF_ENCODERS 1
// #define ENCODERS_PAD_A { B2 }
// #define ENCODERS_PAD_B { B3 }
// #define ENCODERS_PAD_A_RIGHT { F7 }
// #define ENCODERS_PAD_B_RIGHT { F6 }
// #define ENCODER_RESOLUTION 1

