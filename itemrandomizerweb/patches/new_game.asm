;;; VARIA new game hook: skips intro and customizes starting point
;;; 
;;; compile with asar (https://www.smwcentral.net/?a=details&id=14560&p=section),
;;; or a variant of xkas that supports arch directive

arch snes.cpu
lorom

;;; CONSTANTS
!GameStartState = $7ED914


;;; HIJACKS (bank 82 init routines)

org $82801d
    jsl startup

org $828067
    jsl gameplay_start

;;; This skips the intro : game state 1F instead of 1E
org $82eeda
    db $1f

;;; DATA in bank A1 (start options)

org $a1f200
print "start_location: ", pc
start_location:
    ;; start location: $0000=Zebes, $0001=Ceres,
    ;; otherwise hi byte is area and low is save index
    dw $0000
opt_door:
    ;; optional door to open (defaults to construction zone)
    dw $0032

warnpc $a1f20f

;;; CODE in bank A1
org $a1f210
;;; zero flag set if we're starting a new game
;;; called from credits_varia as well
print "check_new_game: ", pc
check_new_game:
    ;; Make sure game mode is 1f
    lda $7e0998
    cmp #$001f : bne .end
    ;; check that Game time and frames is equal zero for new game
    ;; (Thanks Smiley and P.JBoy from metconst)
    lda $09DA
    ora $09DC
    ora $09DE
    ora $09E0
.end:
    rtl

startup:
    jsl check_new_game      : bne .end
    lda.l start_location    : beq .zebes
    cmp #$0001              : beq .ceres
    ;; custom start point on Zebes
    pha
    and #$ff00 : xba : sta $079f ; hi byte is area
    pla
    and #$00ff : sta $078b      ; low byte is save index
    lda #$0000 : jsl $8081fa    ; wake zebes
.zebes:
    lda #$0005 : bra .store_state
.ceres:
    lda #$001f
.store_state:
    sta !GameStartState
.end:
    ;; run hijacked code and return
    lda !GameStartState
    rtl

gameplay_start:
    phx
    jsl check_new_game  : bne .end
	;; lda $7ed8b6 : ora.w #$0004 : sta $7ed8b6
    ;; Set red tower elevator door to blue
    lda $7ed8b2 : ora.w #$0001 : sta $7ed8b2
    ;; Set optional door to blue if necessary
    lda.l opt_door : beq .end
    jsl $80818e		    ; call bit index function, returns X=byte index, $05e7=bitmask
    ;; Set door in bitfield
    lda $7ED8B0,x
    ora $05E7
    sta $7ED8B0,x

    ;; Call the save code to create a new file
    lda $7e0952 : jsl $818000
.end:
    plx
    rtl

warnpc $a1ffff

;; org $80c527
;; crateria_load:
;;     dw $99BD, $8B1A, $0000, $0000, $0000, $0078, $0040
