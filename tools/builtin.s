	.text
	.file	"builtin.c"
	.globl	print                   # -- Begin function print
	.p2align	2
	.type	print,@function
print:                                  # @print
	.cfi_startproc
# %bb.0:
	addi	sp, sp, -16
	.cfi_def_cfa_offset 16
	sw	ra, 12(sp)
	.cfi_offset ra, -4
	mv	a1, a0
	lui	a0, %hi(.L.str)
	addi	a0, a0, %lo(.L.str)
	call	printf
	lw	ra, 12(sp)
	.cfi_restore ra
	addi	sp, sp, 16
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
	.cfi_def_cfa_offset 0
	tail	puts
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
	addi	sp, sp, -16
	.cfi_def_cfa_offset 16
	sw	ra, 12(sp)
	.cfi_offset ra, -4
	mv	a1, a0
	lui	a0, %hi(.L.str.2)
	addi	a0, a0, %lo(.L.str.2)
	call	printf
	lw	ra, 12(sp)
	.cfi_restore ra
	addi	sp, sp, 16
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
	.cfi_offset ra, -4
	mv	a1, a0
	lui	a0, %hi(.L.str.3)
	addi	a0, a0, %lo(.L.str.3)
	call	printf
	lw	ra, 12(sp)
	.cfi_restore ra
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
	.cfi_offset ra, -4
	sw	zero, 8(sp)
	lui	a0, %hi(.L.str.2)
	addi	a0, a0, %lo(.L.str.2)
	addi	a1, sp, 8
	call	__isoc99_scanf
	lw	a0, 8(sp)
	lw	ra, 12(sp)
	.cfi_restore ra
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
	addi	sp, sp, -144
	.cfi_def_cfa_offset 144
	sw	ra, 140(sp)
	sw	s0, 136(sp)
	sw	s1, 132(sp)
	.cfi_offset ra, -4
	.cfi_offset s0, -8
	.cfi_offset s1, -12
	lui	a0, %hi(.L.str)
	addi	a0, a0, %lo(.L.str)
	mv	s0, sp
	mv	a1, s0
	call	__isoc99_scanf
	mv	a0, s0
	call	strlen
	mv	s1, a0
	addi	a0, a0, 4
	srai	a1, a0, 31
	call	malloc
	sw	s1, 0(a0)
	addi	s1, a0, 4
	mv	a0, s1
	mv	a1, s0
	call	strcpy
	mv	a0, s1
	lw	s1, 132(sp)
	lw	s0, 136(sp)
	lw	ra, 140(sp)
	.cfi_restore ra
	.cfi_restore s0
	.cfi_restore s1
	addi	sp, sp, 144
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
	addi	sp, sp, -208
	.cfi_def_cfa_offset 208
	sw	ra, 204(sp)
	sw	s0, 200(sp)
	sw	s1, 196(sp)
	sw	s2, 192(sp)
	sw	s3, 188(sp)
	sw	s4, 184(sp)
	sw	s5, 180(sp)
	sw	s6, 176(sp)
	sw	s7, 172(sp)
	sw	s8, 168(sp)
	sw	s9, 164(sp)
	sw	s10, 160(sp)
	sw	s11, 156(sp)
	.cfi_offset ra, -4
	.cfi_offset s0, -8
	.cfi_offset s1, -12
	.cfi_offset s2, -16
	.cfi_offset s3, -20
	.cfi_offset s4, -24
	.cfi_offset s5, -28
	.cfi_offset s6, -32
	.cfi_offset s7, -36
	.cfi_offset s8, -40
	.cfi_offset s9, -44
	.cfi_offset s10, -48
	.cfi_offset s11, -52
	mv	s2, a0
	srai	a0, a0, 31
	add	a1, s2, a0
	xor	a0, a1, a0
	lui	a1, 419430
	addi	a1, a1, 1639
	addi	a6, zero, 10
	addi	s3, sp, 80
	addi	a3, zero, 18
	mv	s4, zero
	mv	s0, zero
.LBB6_1:                                # =>This Inner Loop Header: Depth=1
	mv	s1, s4
	mulh	a4, a0, a1
	srli	a5, a4, 31
	srai	a4, a4, 2
	add	a4, a4, a5
	mul	a5, a4, a6
	sub	a5, a0, a5
	add	a2, s3, s4
	sb	a5, 0(a2)
	addi	s4, s4, 1
	sltu	a2, s4, s1
	add	s0, s0, a2
	addi	a2, a0, 9
	mv	a0, a4
	bltu	a3, a2, .LBB6_1
# %bb.2:
	addi	a0, zero, 64
	mv	a1, zero
	call	malloc
	srli	t5, s2, 31
	add	a1, t5, s4
	sw	a1, 0(a0)
	addi	t4, a0, 4
	beqz	t5, .LBB6_4
# %bb.3:
	addi	a1, zero, 45
	sb	a1, 0(t4)
.LBB6_4:
	beqz	s0, .LBB6_13
# %bb.5:
	snez	a1, s0
	beqz	a1, .LBB6_14
.LBB6_6:
	lui	a1, 524288
	addi	a1, a1, -1
	and	a0, s0, a1
	andi	a1, s4, -32
	addi	a2, a1, -32
	sw	a1, 4(sp)
	sltu	a1, a2, a1
	sw	a0, 8(sp)
	add	a1, a0, a1
	addi	a1, a1, -1
	slli	a0, a1, 27
	srli	a4, a2, 5
	or	a0, a4, a0
	addi	a4, a0, 1
	or	a2, a2, a1
	andi	a3, a4, 1
	sw	a3, 0(sp)
	beqz	a2, .LBB6_17
# %bb.7:
	sltu	a0, a4, a0
	srli	a1, a1, 5
	add	a1, a1, a0
	sub	a0, a4, a3
	sltu	a4, a4, a3
	sub	a3, a1, a4
	mv	a5, zero
	mv	a4, zero
.LBB6_8:                                # =>This Inner Loop Header: Depth=1
	sw	a0, 68(sp)
	sw	a3, 72(sp)
	sw	a4, 76(sp)
	sub	a1, s1, a5
	add	a4, s3, a1
	or	a1, a5, t5
	add	a1, t4, a1
	lb	a0, 0(a4)
	sw	a0, 60(sp)
	lb	a0, -1(a4)
	sw	a0, 56(sp)
	lb	a0, -2(a4)
	sw	a0, 52(sp)
	lb	a0, -3(a4)
	sw	a0, 48(sp)
	lb	a0, -4(a4)
	sw	a0, 44(sp)
	lb	a0, -5(a4)
	sw	a0, 40(sp)
	lb	a0, -6(a4)
	sw	a0, 36(sp)
	lb	a0, -7(a4)
	sw	a0, 32(sp)
	lb	a0, -8(a4)
	sw	a0, 28(sp)
	lb	a0, -9(a4)
	sw	a0, 24(sp)
	lb	a0, -10(a4)
	sw	a0, 20(sp)
	lb	a0, -11(a4)
	sw	a0, 16(sp)
	lb	a0, -12(a4)
	sw	a0, 12(sp)
	lb	t3, -13(a4)
	lb	t2, -14(a4)
	lb	t0, -15(a4)
	lb	a7, -16(a4)
	sw	a5, 64(sp)
	lb	a6, -17(a4)
	lb	a0, -18(a4)
	lb	a2, -19(a4)
	lb	a3, -20(a4)
	lb	t6, -21(a4)
	lb	s2, -22(a4)
	lb	s5, -23(a4)
	lb	t1, -24(a4)
	lb	s6, -25(a4)
	lb	s9, -26(a4)
	lb	s7, -27(a4)
	lb	s8, -28(a4)
	lb	s10, -29(a4)
	lb	s11, -30(a4)
	lb	a4, -31(a4)
	addi	a4, a4, 48
	sb	a4, 31(a1)
	addi	a4, s11, 48
	sb	a4, 30(a1)
	addi	a4, s10, 48
	sb	a4, 29(a1)
	addi	a4, s8, 48
	sb	a4, 28(a1)
	addi	a4, s7, 48
	sb	a4, 27(a1)
	addi	a4, s9, 48
	sb	a4, 26(a1)
	addi	a4, s6, 48
	sb	a4, 25(a1)
	addi	a4, t1, 48
	sb	a4, 24(a1)
	addi	a4, s5, 48
	sb	a4, 23(a1)
	addi	a4, s2, 48
	sb	a4, 22(a1)
	addi	a4, t6, 48
	sb	a4, 21(a1)
	addi	a4, a3, 48
	sb	a4, 20(a1)
	addi	a4, a2, 48
	sb	a4, 19(a1)
	addi	a4, a0, 48
	sb	a4, 18(a1)
	addi	a4, a6, 48
	sb	a4, 17(a1)
	addi	a0, a7, 48
	sb	a0, 16(a1)
	addi	a0, t0, 48
	sb	a0, 15(a1)
	addi	a0, t2, 48
	sb	a0, 14(a1)
	addi	a0, t3, 48
	sb	a0, 13(a1)
	lw	a0, 12(sp)
	addi	a0, a0, 48
	sb	a0, 12(a1)
	lw	a0, 16(sp)
	addi	a0, a0, 48
	sb	a0, 11(a1)
	lw	a0, 20(sp)
	addi	a0, a0, 48
	sb	a0, 10(a1)
	lw	a0, 24(sp)
	addi	a0, a0, 48
	sb	a0, 9(a1)
	lw	a0, 28(sp)
	addi	a0, a0, 48
	sb	a0, 8(a1)
	lw	a0, 32(sp)
	addi	a0, a0, 48
	sb	a0, 7(a1)
	lw	a0, 36(sp)
	addi	a0, a0, 48
	sb	a0, 6(a1)
	lw	a0, 40(sp)
	addi	a0, a0, 48
	sb	a0, 5(a1)
	lw	a0, 44(sp)
	addi	a0, a0, 48
	sb	a0, 4(a1)
	lw	a0, 48(sp)
	addi	a0, a0, 48
	sb	a0, 3(a1)
	lw	a0, 52(sp)
	addi	a0, a0, 48
	sb	a0, 2(a1)
	lw	a0, 56(sp)
	addi	a0, a0, 48
	sb	a0, 1(a1)
	lw	a0, 60(sp)
	addi	a0, a0, 48
	sb	a0, 0(a1)
	ori	a0, a5, 32
	sub	a1, s1, a0
	add	a4, s3, a1
	or	a0, a0, t5
	add	a1, t4, a0
	lb	a0, 0(a4)
	sw	a0, 60(sp)
	lb	a0, -1(a4)
	sw	a0, 56(sp)
	lb	a0, -2(a4)
	sw	a0, 52(sp)
	lb	a0, -3(a4)
	sw	a0, 48(sp)
	lb	a0, -4(a4)
	sw	a0, 44(sp)
	lb	a0, -5(a4)
	sw	a0, 40(sp)
	lb	a0, -6(a4)
	sw	a0, 36(sp)
	lb	a0, -7(a4)
	sw	a0, 32(sp)
	lb	a0, -8(a4)
	sw	a0, 28(sp)
	lb	a0, -9(a4)
	sw	a0, 24(sp)
	lb	a0, -10(a4)
	sw	a0, 20(sp)
	lb	a0, -11(a4)
	sw	a0, 16(sp)
	lb	s7, -12(a4)
	lb	s8, -13(a4)
	lb	s9, -14(a4)
	lb	s10, -15(a4)
	lb	s11, -16(a4)
	lb	s6, -17(a4)
	lb	s5, -18(a4)
	lb	s2, -19(a4)
	lb	t6, -20(a4)
	lb	t1, -21(a4)
	mv	a3, s3
	lb	s3, -22(a4)
	lb	t0, -23(a4)
	lb	t2, -24(a4)
	lb	a7, -25(a4)
	lb	t3, -26(a4)
	lb	a6, -27(a4)
	mv	a2, t4
	lb	t4, -28(a4)
	lb	a5, -29(a4)
	lb	a0, -30(a4)
	lb	a4, -31(a4)
	addi	a4, a4, 48
	sb	a4, 31(a1)
	lw	a4, 76(sp)
	addi	a0, a0, 48
	sb	a0, 30(a1)
	addi	a0, a5, 48
	sb	a0, 29(a1)
	addi	a0, t4, 48
	mv	t4, a2
	sb	a0, 28(a1)
	addi	a0, a6, 48
	sb	a0, 27(a1)
	addi	a0, t3, 48
	sb	a0, 26(a1)
	addi	a0, a7, 48
	sb	a0, 25(a1)
	addi	a0, t2, 48
	sb	a0, 24(a1)
	addi	a0, t0, 48
	sb	a0, 23(a1)
	addi	a0, s3, 48
	mv	s3, a3
	sb	a0, 22(a1)
	addi	a0, t1, 48
	sb	a0, 21(a1)
	addi	a0, t6, 48
	sb	a0, 20(a1)
	addi	a0, s2, 48
	sb	a0, 19(a1)
	addi	a0, s5, 48
	sb	a0, 18(a1)
	addi	a0, s6, 48
	sb	a0, 17(a1)
	addi	a0, s11, 48
	sb	a0, 16(a1)
	addi	a0, s10, 48
	sb	a0, 15(a1)
	addi	a0, s9, 48
	sb	a0, 14(a1)
	addi	a0, s8, 48
	sb	a0, 13(a1)
	addi	a0, s7, 48
	sb	a0, 12(a1)
	lw	a0, 16(sp)
	addi	a0, a0, 48
	sb	a0, 11(a1)
	lw	a0, 20(sp)
	addi	a0, a0, 48
	sb	a0, 10(a1)
	lw	a0, 24(sp)
	addi	a0, a0, 48
	sb	a0, 9(a1)
	lw	a0, 28(sp)
	addi	a0, a0, 48
	sb	a0, 8(a1)
	lw	a0, 32(sp)
	addi	a0, a0, 48
	sb	a0, 7(a1)
	lw	a0, 36(sp)
	addi	a0, a0, 48
	sb	a0, 6(a1)
	lw	a0, 40(sp)
	addi	a0, a0, 48
	sb	a0, 5(a1)
	lw	a0, 44(sp)
	addi	a0, a0, 48
	sb	a0, 4(a1)
	lw	a0, 48(sp)
	addi	a0, a0, 48
	sb	a0, 3(a1)
	lw	a0, 52(sp)
	addi	a0, a0, 48
	sb	a0, 2(a1)
	lw	a0, 56(sp)
	addi	a0, a0, 48
	sb	a0, 1(a1)
	lw	a0, 60(sp)
	addi	a0, a0, 48
	sb	a0, 0(a1)
	lw	a0, 64(sp)
	addi	a1, a0, 64
	sltu	a0, a1, a0
	add	a4, a4, a0
	lw	a2, 68(sp)
	addi	a0, a2, -2
	sltu	a2, a0, a2
	lw	a3, 72(sp)
	add	a2, a3, a2
	addi	a3, a2, -1
	or	a2, a0, a3
	mv	a5, a1
	bnez	a2, .LBB6_8
# %bb.9:
	lw	a0, 0(sp)
	beqz	a0, .LBB6_11
.LBB6_10:
	sub	a0, s1, a1
	add	a0, s3, a0
	or	a1, a1, t5
	add	a1, t4, a1
	lb	a2, 0(a0)
	sw	a2, 76(sp)
	lb	a2, -1(a0)
	sw	a2, 72(sp)
	lb	a2, -2(a0)
	sw	a2, 68(sp)
	lb	a2, -3(a0)
	sw	a2, 64(sp)
	lb	a2, -4(a0)
	sw	a2, 60(sp)
	lb	a2, -5(a0)
	sw	a2, 56(sp)
	lb	a2, -6(a0)
	sw	a2, 52(sp)
	lb	a2, -7(a0)
	sw	a2, 48(sp)
	lb	a2, -8(a0)
	sw	a2, 44(sp)
	lb	a2, -9(a0)
	sw	a2, 40(sp)
	lb	s3, -10(a0)
	lb	s5, -11(a0)
	lb	s6, -12(a0)
	lb	s7, -13(a0)
	lb	s8, -14(a0)
	lb	s9, -15(a0)
	lb	s10, -16(a0)
	lb	s11, -17(a0)
	lb	s2, -18(a0)
	lb	t6, -19(a0)
	lb	s1, -20(a0)
	lb	a3, -21(a0)
	lb	t3, -22(a0)
	lb	t2, -23(a0)
	lb	t1, -24(a0)
	lb	t0, -25(a0)
	lb	a7, -26(a0)
	lb	a6, -27(a0)
	lb	a5, -28(a0)
	lb	a4, -29(a0)
	lb	a2, -30(a0)
	lb	a0, -31(a0)
	addi	a0, a0, 48
	sb	a0, 31(a1)
	addi	a0, a2, 48
	sb	a0, 30(a1)
	addi	a0, a4, 48
	sb	a0, 29(a1)
	addi	a0, a5, 48
	sb	a0, 28(a1)
	addi	a0, a6, 48
	sb	a0, 27(a1)
	addi	a0, a7, 48
	sb	a0, 26(a1)
	addi	a0, t0, 48
	sb	a0, 25(a1)
	addi	a0, t1, 48
	sb	a0, 24(a1)
	addi	a0, t2, 48
	sb	a0, 23(a1)
	addi	a0, t3, 48
	sb	a0, 22(a1)
	addi	a0, a3, 48
	sb	a0, 21(a1)
	addi	a0, s1, 48
	sb	a0, 20(a1)
	addi	a0, t6, 48
	sb	a0, 19(a1)
	addi	a0, s2, 48
	sb	a0, 18(a1)
	addi	a0, s11, 48
	sb	a0, 17(a1)
	addi	a0, s10, 48
	sb	a0, 16(a1)
	addi	a0, s9, 48
	sb	a0, 15(a1)
	addi	a0, s8, 48
	sb	a0, 14(a1)
	addi	a0, s7, 48
	sb	a0, 13(a1)
	addi	a0, s6, 48
	sb	a0, 12(a1)
	addi	a0, s5, 48
	sb	a0, 11(a1)
	addi	a0, s3, 48
	addi	s3, sp, 80
	sb	a0, 10(a1)
	lw	a0, 40(sp)
	addi	a0, a0, 48
	sb	a0, 9(a1)
	lw	a0, 44(sp)
	addi	a0, a0, 48
	sb	a0, 8(a1)
	lw	a0, 48(sp)
	addi	a0, a0, 48
	sb	a0, 7(a1)
	lw	a0, 52(sp)
	addi	a0, a0, 48
	sb	a0, 6(a1)
	lw	a0, 56(sp)
	addi	a0, a0, 48
	sb	a0, 5(a1)
	lw	a0, 60(sp)
	addi	a0, a0, 48
	sb	a0, 4(a1)
	lw	a0, 64(sp)
	addi	a0, a0, 48
	sb	a0, 3(a1)
	lw	a0, 68(sp)
	addi	a0, a0, 48
	sb	a0, 2(a1)
	lw	a0, 72(sp)
	addi	a0, a0, 48
	sb	a0, 1(a1)
	lw	a0, 76(sp)
	addi	a0, a0, 48
	sb	a0, 0(a1)
.LBB6_11:
	lw	a4, 4(sp)
	xor	a0, s4, a4
	lw	a3, 8(sp)
	xor	a1, s0, a3
	or	a0, a0, a1
	beqz	a0, .LBB6_16
# %bb.12:
	sub	a0, s0, a3
	sltu	a1, s4, a4
	sub	s0, a0, a1
	sub	s4, s4, a4
	j	.LBB6_15
.LBB6_13:
	addi	a1, zero, 31
	sltu	a1, a1, s4
	bnez	a1, .LBB6_6
.LBB6_14:
	mv	a4, zero
	mv	a3, zero
.LBB6_15:                               # =>This Inner Loop Header: Depth=1
	add	a0, a4, t5
	add	a0, t4, a0
	addi	a1, s4, -1
	add	a2, s3, a1
	lb	a2, 0(a2)
	addi	a2, a2, 48
	sb	a2, 0(a0)
	addi	a0, a4, 1
	sltu	a2, a0, a4
	add	a3, a3, a2
	sltu	a2, a1, s4
	add	a2, s0, a2
	addi	s0, a2, -1
	or	a2, a1, s0
	mv	a4, a0
	mv	s4, a1
	bnez	a2, .LBB6_15
.LBB6_16:
	mv	a0, t4
	lw	s11, 156(sp)
	lw	s10, 160(sp)
	lw	s9, 164(sp)
	lw	s8, 168(sp)
	lw	s7, 172(sp)
	lw	s6, 176(sp)
	lw	s5, 180(sp)
	lw	s4, 184(sp)
	lw	s3, 188(sp)
	lw	s2, 192(sp)
	lw	s1, 196(sp)
	lw	s0, 200(sp)
	lw	ra, 204(sp)
	.cfi_restore ra
	.cfi_restore s0
	.cfi_restore s1
	.cfi_restore s2
	.cfi_restore s3
	.cfi_restore s4
	.cfi_restore s5
	.cfi_restore s6
	.cfi_restore s7
	.cfi_restore s8
	.cfi_restore s9
	.cfi_restore s10
	.cfi_restore s11
	addi	sp, sp, 208
	.cfi_def_cfa_offset 0
	ret
.LBB6_17:
	mv	a1, zero
	lw	a0, 0(sp)
	bnez	a0, .LBB6_10
	j	.LBB6_11
.Lfunc_end6:
	.size	toString, .Lfunc_end6-toString
	.cfi_endproc
                                        # -- End function
	.globl	_string_substring       # -- Begin function _string_substring
	.p2align	2
	.type	_string_substring,@function
_string_substring:                      # @_string_substring
	.cfi_startproc
# %bb.0:
	addi	sp, sp, -32
	.cfi_def_cfa_offset 32
	sw	ra, 28(sp)
	sw	s0, 24(sp)
	sw	s1, 20(sp)
	sw	s2, 16(sp)
	sw	s3, 12(sp)
	sw	s4, 8(sp)
	.cfi_offset ra, -4
	.cfi_offset s0, -8
	.cfi_offset s1, -12
	.cfi_offset s2, -16
	.cfi_offset s3, -20
	.cfi_offset s4, -24
	mv	s4, a2
	mv	s1, a1
	mv	s2, a0
	sub	s0, a2, a1
	addi	a0, s0, 4
	srai	a1, a0, 31
	call	malloc
	sw	s0, 0(a0)
	addi	s3, a0, 4
	bge	s1, s4, .LBB7_2
# %bb.1:
	add	a1, s2, s1
	mv	a0, s3
	mv	a2, s0
	call	memcpy
.LBB7_2:
	mv	a0, s3
	lw	s4, 8(sp)
	lw	s3, 12(sp)
	lw	s2, 16(sp)
	lw	s1, 20(sp)
	lw	s0, 24(sp)
	lw	ra, 28(sp)
	.cfi_restore ra
	.cfi_restore s0
	.cfi_restore s1
	.cfi_restore s2
	.cfi_restore s3
	.cfi_restore s4
	addi	sp, sp, 32
	.cfi_def_cfa_offset 0
	ret
.Lfunc_end7:
	.size	_string_substring, .Lfunc_end7-_string_substring
	.cfi_endproc
                                        # -- End function
	.globl	_string_parseInt        # -- Begin function _string_parseInt
	.p2align	2
	.type	_string_parseInt,@function
_string_parseInt:                       # @_string_parseInt
	.cfi_startproc
# %bb.0:
	lbu	a1, 0(a0)
	addi	a2, a1, -48
	andi	a2, a2, 255
	addi	a3, zero, 9
	bltu	a3, a2, .LBB8_4
# %bb.1:                                # %.preheader
	addi	a3, a0, 1
	addi	a2, zero, 10
	mv	a0, zero
.LBB8_2:                                # =>This Inner Loop Header: Depth=1
	mul	a0, a0, a2
	slli	a1, a1, 24
	srai	a1, a1, 24
	add	a0, a0, a1
	addi	a4, a3, 1
	addi	a0, a0, -48
	lbu	a1, 0(a3)
	addi	a3, a1, -48
	andi	a5, a3, 255
	mv	a3, a4
	bltu	a5, a2, .LBB8_2
# %bb.3:
	.cfi_def_cfa_offset 0
	ret
.LBB8_4:
	mv	a0, zero
	.cfi_def_cfa_offset 0
	ret
.Lfunc_end8:
	.size	_string_parseInt, .Lfunc_end8-_string_parseInt
	.cfi_endproc
                                        # -- End function
	.globl	_string_ord             # -- Begin function _string_ord
	.p2align	2
	.type	_string_ord,@function
_string_ord:                            # @_string_ord
	.cfi_startproc
# %bb.0:
	add	a0, a0, a1
	lb	a0, 0(a0)
	.cfi_def_cfa_offset 0
	ret
.Lfunc_end9:
	.size	_string_ord, .Lfunc_end9-_string_ord
	.cfi_endproc
                                        # -- End function
	.globl	_string_add             # -- Begin function _string_add
	.p2align	2
	.type	_string_add,@function
_string_add:                            # @_string_add
	.cfi_startproc
# %bb.0:
	addi	sp, sp, -32
	.cfi_def_cfa_offset 32
	sw	ra, 28(sp)
	sw	s0, 24(sp)
	sw	s1, 20(sp)
	sw	s2, 16(sp)
	sw	s3, 12(sp)
	.cfi_offset ra, -4
	.cfi_offset s0, -8
	.cfi_offset s1, -12
	.cfi_offset s2, -16
	.cfi_offset s3, -20
	mv	s2, a1
	mv	s1, a0
	lw	s3, -4(a0)
	lw	a0, -4(a1)
	add	s0, a0, s3
	addi	a0, s0, 4
	srai	a1, a0, 31
	call	malloc
	sw	s0, 0(a0)
	addi	s0, a0, 4
	mv	a0, s0
	mv	a1, s1
	call	strcpy
	add	a0, s0, s3
	mv	a1, s2
	call	strcpy
	mv	a0, s0
	lw	s3, 12(sp)
	lw	s2, 16(sp)
	lw	s1, 20(sp)
	lw	s0, 24(sp)
	lw	ra, 28(sp)
	.cfi_restore ra
	.cfi_restore s0
	.cfi_restore s1
	.cfi_restore s2
	.cfi_restore s3
	addi	sp, sp, 32
	.cfi_def_cfa_offset 0
	ret
.Lfunc_end10:
	.size	_string_add, .Lfunc_end10-_string_add
	.cfi_endproc
                                        # -- End function
	.type	.L.str,@object          # @.str
	.section	.rodata.str1.1,"aMS",@progbits,1
.L.str:
	.asciz	"%s"
	.size	.L.str, 3

	.type	.L.str.2,@object        # @.str.2
.L.str.2:
	.asciz	"%d"
	.size	.L.str.2, 3

	.type	.L.str.3,@object        # @.str.3
.L.str.3:
	.asciz	"%d\n"
	.size	.L.str.3, 4


	.ident	"clang version 9.0.0-2~ubuntu18.04.2 (tags/RELEASE_900/final)"
	.section	".note.GNU-stack","",@progbits
