;;; compile with asar v1.81 (https://github.com/RPGHacker/asar/releases/tag/v1.81)

;;; Super Metroid save/load routine expansion v1.0
;;; Made by Scyzer
;;; 
;;; **Free space used from $81:EF20 (0x00EF20) to $81:F0A4 (0x00F0A4)**
;;; 
;;; This patch/asm file will modify the saving and loading routine of Super Metroid for the SNES.
;;; The most basic function is that is will change how maps are stored and loaded, meaning you will be able to use the ENTIRE map for all areas.
;;; Debug is still not supported due to space limitations, but there is no map for this area anyway, so...
;;; 
;;; KejMap is made completely redundant by this patch, so dont bother applying it (it won't do anything if you already have)
;;; 
;;; There's a few other bits and pieces for more experienced hackers:
;;; 	$100 bytes of ram from $7F:FE00 to $7F:FEFF is saved per file.
;;; 		You can modify this ram, and it will still be the same when you load the game.
;;; 	$100 bytes of ram from $7F:FF00 to $7F:FFFF is saved GLOBALLY.
;;; 		Any ram here will apply to ALL 3 save game files (including if you clear all save games). Deleting the .srm file will remove these changes.

lorom

org $819A47		;Fix File Copy for the new SRAM files
	LDA.l SRAMAddressTable,X : skip 7 : LDA.l SRAMAddressTable,X : skip 11 : CPY #$0A00
org $819CAE		;Fix File Clear for the new SRAM files
	LDA.l SRAMAddressTable,X : skip 12 : CPY #$0A00

org $818000
	JMP SaveGame
org $818085
	JMP LoadGame

;;; relocate after credits_varia
org $81f6ff
SRAMAddressTable:
	DW $0010,$0A10,$1410
CheckSumAdd: CLC : ADC $14 : INC A : STA $14 : RTS

SaveGame: PHP : REP #$30 : PHB : PHX : PHY
	PEA $7E7E : PLB : PLB : STZ $14 : AND #$0003 : ASL A : STA $12
	LDA $079F : INC A : XBA : TAX : LDY #$00FE
SaveMap: LDA $07F7,Y : STA $CD50,X : DEX : DEX : DEY : DEY : BPL SaveMap		;Saves the current map
	LDY #$005E
SaveItems: LDA $09A2,Y : STA $D7C0,Y : DEY : DEY : BPL SaveItems				;Saves current equipment	
	LDA $078B : STA $D916		;Current save for the area
	LDA $079F : STA $D918		;Current Area
	LDX $12 : LDA.l SRAMAddressTable,X : TAX : LDY #$0000		;Where to save for items and event bits
SaveSRAMItems: LDA $D7C0,Y : STA $700000,X : JSR CheckSumAdd : INX : INX : INY : INY : CPY #$0160 : BNE SaveSRAMItems	
	LDY #$06FE		;How much data to save for maps
SaveSRAMMaps: LDA $CD52,Y : STA $700000,X : INX : INX : DEY : DEY : BPL SaveSRAMMaps	
	PEA $7F7F : PLB : PLB : LDY #$00FE		;How much extra data to save per save
SaveSRAMExtra: LDA $FE00,Y : STA $700000,X : INX : INX : DEY : DEY : BPL SaveSRAMExtra
	LDY #$00FE : LDX #$1E10					;How much extra data to save globally (affects all saves)
SaveSRAMExtraA: LDA $FF00,Y : STA $700000,X : INX : INX : DEY : DEY : BPL SaveSRAMExtraA
SaveChecksum: LDX $12 : LDA $14 : STA $700000,X : STA $701FF0,X : EOR #$FFFF : STA $700008,X : STA $701FF8,X
EndSaveGame: PLY : PLX : PLB : PLP : RTL

LoadGame: PHP : REP #$30 : PHB : PHX : PHY
	PEA $7E7E : PLB : PLB : STZ $14 : AND #$0003 : ASL A : STA $12
	TAX : LDA.l SRAMAddressTable,X : STA $16 : TAX : LDY #$0000		;How much data to load for items and event bits
LoadSRAMItems: LDA $700000,X : STA $D7C0,Y : JSR CheckSumAdd : INX : INX : INY : INY : CPY #$0160 : BNE LoadSRAMItems	
	LDY #$06FE		;How much data to load for maps
LoadSRAMMaps: LDA $700000,X : STA $CD52,Y : INX : INX : DEY : DEY : BPL LoadSRAMMaps
	PEA $7F7F : PLB : PLB : LDY #$00FE		;How much extra data to load per save
LoadSRAMExtra: LDA $700000,X : STA $FE00,Y : INX : INX : DEY : DEY : BPL LoadSRAMExtra
	LDY #$00FE : LDX #$1E10					;How much extra data to load globally (affects all saves)
LoadSRAMExtraA: LDA $700000,X : STA $FF00,Y : INX : INX : DEY : DEY : BPL LoadSRAMExtraA
LoadCheckSum: LDX $12 : LDA $700000,X : CMP $14 : BNE $0B : EOR #$FFFF : CMP $14 : BNE $02 : BRA LoadSRAM
	LDA $14 : CMP $701FF0,X : BNE SetupClearSRAM : EOR #$FFFF : CMP $701FF8,X : BNE SetupClearSRAM : BRA LoadSRAM
LoadSRAM: PEA $7E7E : PLB : PLB : LDY #$005E
LoadItems: LDA $D7C0,Y : STA $09A2,Y : DEY : DEY : BPL LoadItems		;Loads current equipment	
	LDA $D916 : STA $078B		;Current save for the area
	LDA $D918 : STA $079F		;Current Area
	PLY : PLX : PLB : PLP : CLC : RTL
SetupClearSRAM: LDX $16 : LDY #$09FE : LDA #$0000
ClearSRAM: STA $700000,X : INX : INX : DEY : DEY : BPL ClearSRAM
	PLY : PLX : PLB : PLP : SEC : RTL

print "end: ", pc
warnpc $81f889
