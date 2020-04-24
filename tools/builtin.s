	.text
	.file	"builtin.c"
	.globl	print                   # -- Begin function print
	.p2align	2
	.type	print,@function
print:                                  # @print
	.cfi_startproc
# %bb.0:
	addi	sp, sp, -32
	.cfi_def_cfa_offset 32
	sw	ra, 28(sp)
	sw	s0, 24(sp)
	.cfi_offset ra, -4
	.cfi_offset s0, -8
	addi	s0, sp, 32
	.cfi_def_cfa s0, 0
	sw	a0, -16(s0)
	lw	a0, -16(s0)
	lw	a0, -4(a0)
	sw	a0, -20(s0)
	sw	zero, -24(s0)
	j	.LBB0_1
.LBB0_1:                                # =>This Inner Loop Header: Depth=1
	lw	a0, -24(s0)
	lw	a1, -20(s0)
	bge	a0, a1, .LBB0_4
	j	.LBB0_2
.LBB0_2:                                #   in Loop: Header=BB0_1 Depth=1
	lw	a0, -16(s0)
	lw	a1, -24(s0)
	add	a0, a0, a1
	lb	a0, 0(a0)
	call	putchar
	j	.LBB0_3
.LBB0_3:                                #   in Loop: Header=BB0_1 Depth=1
	lw	a0, -24(s0)
	addi	a0, a0, 1
	sw	a0, -24(s0)
	j	.LBB0_1
.LBB0_4:
	lw	s0, 24(sp)
	.cfi_def_cfa sp, 32
	lw	ra, 28(sp)
	.cfi_restore ra
	.cfi_restore s0
	addi	sp, sp, 32
	.cfi_def_cfa_offset 0
	ret
.Lfunc_end0:
	.size	print, .Lfunc_end0-print
	.cfi_endproc
                                        # -- End function
	.globl	println                 # -- Begin function println
	.p2align	2
	.type	println,@function
println:                                # @println
	.cfi_startproc
# %bb.0:
	addi	sp, sp, -16
	.cfi_def_cfa_offset 16
	sw	ra, 12(sp)
	sw	s0, 8(sp)
	.cfi_offset ra, -4
	.cfi_offset s0, -8
	addi	s0, sp, 16
	.cfi_def_cfa s0, 0
	sw	a0, -16(s0)
	lw	a0, -16(s0)
	call	print
	addi	a0, zero, 10
	call	putchar
	lw	s0, 8(sp)
	.cfi_def_cfa sp, 16
	lw	ra, 12(sp)
	.cfi_restore ra
	.cfi_restore s0
	addi	sp, sp, 16
	.cfi_def_cfa_offset 0
	ret
.Lfunc_end1:
	.size	println, .Lfunc_end1-println
	.cfi_endproc
                                        # -- End function
	.globl	printInt                # -- Begin function printInt
	.p2align	2
	.type	printInt,@function
printInt:                               # @printInt
	.cfi_startproc
# %bb.0:
	addi	sp, sp, -96
	.cfi_def_cfa_offset 96
	sw	ra, 92(sp)
	sw	s0, 88(sp)
	.cfi_offset ra, -4
	.cfi_offset s0, -8
	addi	s0, sp, 96
	.cfi_def_cfa s0, 0
	sw	a0, -12(s0)
	addi	a0, s0, -80
	sw	a0, -88(s0)
	j	.LBB2_1
.LBB2_1:                                # =>This Inner Loop Header: Depth=1
	lw	a0, -12(s0)
	beqz	a0, .LBB2_3
	j	.LBB2_2
.LBB2_2:                                #   in Loop: Header=BB2_1 Depth=1
	lw	a0, -12(s0)
	lui	a1, 419430
	addi	a1, a1, 1639
	mulh	a2, a0, a1
	srli	a3, a2, 31
	srli	a2, a2, 2
	add	a2, a2, a3
	addi	a3, zero, 10
	mul	a2, a2, a3
	sub	a0, a0, a2
	lw	a2, -88(s0)
	addi	a3, a2, 1
	sw	a3, -88(s0)
	sb	a0, 0(a2)
	lw	a0, -12(s0)
	mulh	a0, a0, a1
	srli	a1, a0, 31
	srai	a0, a0, 2
	add	a0, a0, a1
	sw	a0, -12(s0)
	j	.LBB2_1
.LBB2_3:
	j	.LBB2_4
.LBB2_4:                                # =>This Inner Loop Header: Depth=1
	lw	a0, -88(s0)
	addi	a1, s0, -80
	beq	a0, a1, .LBB2_6
	j	.LBB2_5
.LBB2_5:                                #   in Loop: Header=BB2_4 Depth=1
	lw	a0, -88(s0)
	addi	a1, a0, -1
	sw	a1, -88(s0)
	lb	a0, -1(a0)
	addi	a0, a0, 48
	call	putchar
	j	.LBB2_4
.LBB2_6:
	lw	s0, 88(sp)
	.cfi_def_cfa sp, 96
	lw	ra, 92(sp)
	.cfi_restore ra
	.cfi_restore s0
	addi	sp, sp, 96
	.cfi_def_cfa_offset 0
	ret
.Lfunc_end2:
	.size	printInt, .Lfunc_end2-printInt
	.cfi_endproc
                                        # -- End function
	.globl	printlnInt              # -- Begin function printlnInt
	.p2align	2
	.type	printlnInt,@function
printlnInt:                             # @printlnInt
	.cfi_startproc
# %bb.0:
	addi	sp, sp, -16
	.cfi_def_cfa_offset 16
	sw	ra, 12(sp)
	sw	s0, 8(sp)
	.cfi_offset ra, -4
	.cfi_offset s0, -8
	addi	s0, sp, 16
	.cfi_def_cfa s0, 0
	sw	a0, -12(s0)
	lw	a0, -12(s0)
	call	printInt
	addi	a0, zero, 10
	call	putchar
	lw	s0, 8(sp)
	.cfi_def_cfa sp, 16
	lw	ra, 12(sp)
	.cfi_restore ra
	.cfi_restore s0
	addi	sp, sp, 16
	.cfi_def_cfa_offset 0
	ret
.Lfunc_end3:
	.size	printlnInt, .Lfunc_end3-printlnInt
	.cfi_endproc
                                        # -- End function
	.globl	getInt                  # -- Begin function getInt
	.p2align	2
	.type	getInt,@function
getInt:                                 # @getInt
	.cfi_startproc
# %bb.0:
	addi	sp, sp, -16
	.cfi_def_cfa_offset 16
	sw	ra, 12(sp)
	sw	s0, 8(sp)
	.cfi_offset ra, -4
	.cfi_offset s0, -8
	addi	s0, sp, 16
	.cfi_def_cfa s0, 0
	sw	zero, -12(s0)
	lui	a0, %hi(.L.str)
	addi	a0, a0, %lo(.L.str)
	addi	a1, s0, -12
	call	__isoc99_scanf
	lw	a0, -12(s0)
	lw	s0, 8(sp)
	.cfi_def_cfa sp, 16
	lw	ra, 12(sp)
	.cfi_restore ra
	.cfi_restore s0
	addi	sp, sp, 16
	.cfi_def_cfa_offset 0
	ret
.Lfunc_end4:
	.size	getInt, .Lfunc_end4-getInt
	.cfi_endproc
                                        # -- End function
	.globl	getString               # -- Begin function getString
	.p2align	2
	.type	getString,@function
getString:                              # @getString
	.cfi_startproc
# %bb.0:
	addi	sp, sp, -160
	.cfi_def_cfa_offset 160
	sw	ra, 156(sp)
	sw	s0, 152(sp)
	sw	s1, 148(sp)
	.cfi_offset ra, -4
	.cfi_offset s0, -8
	.cfi_offset s1, -12
	addi	s0, sp, 160
	.cfi_def_cfa s0, 0
	lui	a0, %hi(.L.str.1)
	addi	a0, a0, %lo(.L.str.1)
	addi	s1, s0, -144
	mv	a1, s1
	call	__isoc99_scanf
	mv	a0, s1
	call	strlen
	sw	a0, -148(s0)
	lw	a0, -148(s0)
	addi	a0, a0, 4
	srai	a1, a0, 31
	call	malloc
	sw	a0, -152(s0)
	lw	a0, -148(s0)
	lw	a1, -152(s0)
	sw	a0, 0(a1)
	lw	a0, -152(s0)
	addi	a0, a0, 4
	mv	a1, s1
	call	strcpy
	lw	a0, -152(s0)
	addi	a0, a0, 4
	lw	s1, 148(sp)
	lw	s0, 152(sp)
	.cfi_def_cfa sp, 160
	lw	ra, 156(sp)
	.cfi_restore ra
	.cfi_restore s0
	.cfi_restore s1
	addi	sp, sp, 160
	.cfi_def_cfa_offset 0
	ret
.Lfunc_end5:
	.size	getString, .Lfunc_end5-getString
	.cfi_endproc
                                        # -- End function
	.globl	toString                # -- Begin function toString
	.p2align	2
	.type	toString,@function
toString:                               # @toString
	.cfi_startproc
# %bb.0:
	addi	sp, sp, -112
	.cfi_def_cfa_offset 112
	sw	ra, 108(sp)
	sw	s0, 104(sp)
	.cfi_offset ra, -4
	.cfi_offset s0, -8
	addi	s0, sp, 112
	.cfi_def_cfa s0, 0
	sw	a0, -12(s0)
	addi	a0, s0, -80
	sw	a0, -88(s0)
	j	.LBB6_1
.LBB6_1:                                # =>This Inner Loop Header: Depth=1
	lw	a0, -12(s0)
	beqz	a0, .LBB6_3
	j	.LBB6_2
.LBB6_2:                                #   in Loop: Header=BB6_1 Depth=1
	lw	a0, -12(s0)
	lui	a1, 419430
	addi	a1, a1, 1639
	mulh	a2, a0, a1
	srli	a3, a2, 31
	srli	a2, a2, 2
	add	a2, a2, a3
	addi	a3, zero, 10
	mul	a2, a2, a3
	sub	a0, a0, a2
	lw	a2, -88(s0)
	addi	a3, a2, 1
	sw	a3, -88(s0)
	sb	a0, 0(a2)
	lw	a0, -12(s0)
	mulh	a0, a0, a1
	srli	a1, a0, 31
	srai	a0, a0, 2
	add	a0, a0, a1
	sw	a0, -12(s0)
	j	.LBB6_1
.LBB6_3:
	addi	a0, zero, 64
	mv	a1, zero
	call	malloc
	sw	a0, -96(s0)
	lw	a0, -88(s0)
	addi	a1, s0, -80
	sub	a0, a0, a1
	lw	a1, -96(s0)
	sw	a0, 0(a1)
	lw	a0, -96(s0)
	addi	a0, a0, 4
	sw	a0, -96(s0)
	sw	zero, -100(s0)
	j	.LBB6_4
.LBB6_4:                                # =>This Inner Loop Header: Depth=1
	lw	a0, -88(s0)
	addi	a1, s0, -80
	beq	a0, a1, .LBB6_7
	j	.LBB6_5
.LBB6_5:                                #   in Loop: Header=BB6_4 Depth=1
	lw	a0, -88(s0)
	addi	a1, a0, -1
	sw	a1, -88(s0)
	lb	a0, -1(a0)
	lw	a1, -96(s0)
	lw	a2, -100(s0)
	add	a1, a1, a2
	sb	a0, 0(a1)
	j	.LBB6_6
.LBB6_6:                                #   in Loop: Header=BB6_4 Depth=1
	lw	a0, -100(s0)
	addi	a0, a0, 1
	sw	a0, -100(s0)
	j	.LBB6_4
.LBB6_7:
	lw	a0, -96(s0)
	lw	s0, 104(sp)
	.cfi_def_cfa sp, 112
	lw	ra, 108(sp)
	.cfi_restore ra
	.cfi_restore s0
	addi	sp, sp, 112
	.cfi_def_cfa_offset 0
	ret
.Lfunc_end6:
	.size	toString, .Lfunc_end6-toString
	.cfi_endproc
                                        # -- End function
	.type	.L.str,@object          # @.str
	.section	.rodata.str1.1,"aMS",@progbits,1
.L.str:
	.asciz	"%d"
	.size	.L.str, 3

	.type	.L.str.1,@object        # @.str.1
.L.str.1:
	.asciz	"%s"
	.size	.L.str.1, 3


	.ident	"clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final)"
	.section	".note.GNU-stack","",@progbits