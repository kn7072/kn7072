#pragma once

#ifdef VIA_ENABLE
/* VIA configuration. */
#    define DYNAMIC_KEYMAP_LAYER_COUNT 4
#endif // VIA_ENABLE

// #define FORCE_NKRO
#define COMBO_COUNT 10

//  The firmware is too large!
#define COMBO_TERM 300 // timeout period for combos to 40ms.

#define LEADER_TIMEOUT 500
#define QUICK_TAP_TERM 300
#define TAPPING_TERM 300


#define ENCODERS_PAD_A { B2 }
#define ENCODERS_PAD_B { B3 }
#define ENCODER_RESOLUTIONS { 1}
#define ENCODERS_PAD_A_RIGHT { F7 }
#define ENCODERS_PAD_B_RIGHT { F6 }
#define ENCODER_RESOLUTION { 1 }
#define ENCODER_MAP_KEY_DELAY 10

