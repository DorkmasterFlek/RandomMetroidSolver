;;; VARIA shared constants

include

;; shared ROM options addresses
!disabled_tourian_escape_flag = $a1f5fe

;; shared constants
;; RAM to store current obj check index
!obj_check_index = $7fff46

;;; IGT vanilla RAM
!igt_frames = $7E09DA
!igt_seconds = $7E09DC
!igt_minutes = $7E09DE
!igt_hours = $7E09E0

;; RTA timer RAM updated during NMI
!timer1 = $05b8
!timer2 = $05ba

;; stats RAM
!_stats_ram = fc00
!stats_ram = $7f!_stats_ram
!stats_timer = !stats_ram

;; bitfields
; arg: A=bit index. returns: X=byte index, !bitindex_mask=bitmask
!bitindex_routine = $80818e
!bitindex_mask = $05e7
!doors_bitfield = $7ED8B0

;; tracked stats (see tracking.txt)
!stat_nb_door_transitions = #$0002
!stat_rta_door_transitions = #$0003
!stat_rta_door_align = #$0005
!stat_rta_regions = #$0007
!stat_uncharged_shots = #$001f
!stat_charged_shots = #$0020
!stat_SBAs = #$0021
!stat_missiles = #$0022
!stat_supers = #$0023
!stat_PBs = #$0024
!stat_bombs = #$0025
!stat_rta_menu = #$0026
!stat_deaths = #$0028
!stat_resets = #$0029

;; vanilla area check
!area_index = $079f
!brinstar = $0001
!norfair = $0002

!palettes_ram = $7EC000
!palette_size = 32              ; usual size of a palette is 16 colors (1 word per color)

;;; pause state
!pause_index = $0727

;;; pause index values
!pause_index_map_screen = #$0000
!pause_index_equipment_screen = #$0001
!pause_index_map2equip_fading_out = #$0002
!pause_index_map2equip_load_equip = #$0003
!pause_index_map2equip_fading_in = #$0004
!pause_index_equip2map_fading_out = #$0005
!pause_index_equip2map_load_map = #$0006
!pause_index_equip2map_fading_in = #$0007
