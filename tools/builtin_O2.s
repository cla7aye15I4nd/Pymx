	.file	"builtin.c"
	.option nopic
	.text
	.align	2
	.globl	print
	.type	print, @function
print:
	addi	sp,sp,-16
	sw	s1,4(sp)
	lw	s1,-4(a0)
	sw	ra,12(sp)
	sw	s0,8(sp)
	sw	s2,0(sp)
	ble	s1,zero,.L1
	mv	s0,a0
	add	s1,a0,s1
	lui	s2,%hi(stdout)
.L3:
	lbu	a0,0(s0)
	lw	a1,%lo(stdout)(s2)
	addi	s0,s0,1
	call	putc
	bne	s0,s1,.L3
.L1:
	lw	ra,12(sp)
	lw	s0,8(sp)
	lw	s1,4(sp)
	lw	s2,0(sp)
	addi	sp,sp,16
	jr	ra
	.size	print, .-print
	.align	2
	.globl	println
	.type	println, @function
println:
	addi	sp,sp,-16
	sw	ra,12(sp)
	call	print
	lui	a5,%hi(stdout)
	lw	ra,12(sp)
	lw	a1,%lo(stdout)(a5)
	li	a0,10
	addi	sp,sp,16
	tail	putc
	.size	println, .-println
	.align	2
	.globl	printInt
	.type	printInt, @function
printInt:
	addi	sp,sp,-96
	sw	s1,84(sp)
	sw	ra,92(sp)
	sw	s0,88(sp)
	sw	s2,80(sp)
	sw	s3,76(sp)
	mv	s1,a0
	blt	a0,zero,.L16
.L10:
	mv	s2,sp
	mv	s0,s2
	li	a5,10
.L11:
	rem	a0,s1,a5
	addi	s0,s0,1
	div	s1,s1,a5
	andi	a0,a0,0xff
	sb	a0,-1(s0)
	bne	s1,zero,.L11
	beq	s0,s2,.L9
	lui	s3,%hi(stdout)
	j	.L13
.L17:
	lbu	a0,-1(s0)
.L13:
	lw	a1,%lo(stdout)(s3)
	addi	s0,s0,-1
	addi	a0,a0,48
	call	putc
	bne	s0,s2,.L17
.L9:
	lw	ra,92(sp)
	lw	s0,88(sp)
	lw	s1,84(sp)
	lw	s2,80(sp)
	lw	s3,76(sp)
	addi	sp,sp,96
	jr	ra
.L16:
	lui	s3,%hi(stdout)
	lw	a1,%lo(stdout)(s3)
	li	a0,45
	neg	s1,s1
	call	putc
	j	.L10
	.size	printInt, .-printInt
	.align	2
	.globl	printlnInt
	.type	printlnInt, @function
printlnInt:
	addi	sp,sp,-16
	sw	ra,12(sp)
	call	printInt
	lui	a5,%hi(stdout)
	lw	ra,12(sp)
	lw	a1,%lo(stdout)(a5)
	li	a0,10
	addi	sp,sp,16
	tail	putc
	.size	printlnInt, .-printlnInt
	.section	.rodata.str1.4,"aMS",@progbits,1
	.align	2
.LC0:
	.string	"%d"
	.text
	.align	2
	.globl	getInt
	.type	getInt, @function
getInt:
	addi	sp,sp,-32
	lui	a0,%hi(.LC0)
	addi	a1,sp,12
	addi	a0,a0,%lo(.LC0)
	sw	ra,28(sp)
	sw	zero,12(sp)
	call	__isoc99_scanf
	lw	ra,28(sp)
	lw	a0,12(sp)
	addi	sp,sp,32
	jr	ra
	.size	getInt, .-getInt
	.section	.rodata.str1.4
	.align	2
.LC1:
	.string	"%s"
	.text
	.align	2
	.globl	getString
	.type	getString, @function
getString:
	addi	sp,sp,-144
	lui	a0,%hi(.LC1)
	mv	a1,sp
	addi	a0,a0,%lo(.LC1)
	sw	ra,140(sp)
	sw	s0,136(sp)
	call	__isoc99_scanf
	mv	a0,sp
	call	strlen
	mv	s0,a0
	addi	a0,a0,4
	call	malloc
	mv	a5,a0
	addi	a4,a0,4
	addi	a2,s0,1
	mv	a1,sp
	sw	s0,0(a5)
	mv	a0,a4
	call	memcpy
	lw	ra,140(sp)
	lw	s0,136(sp)
	addi	sp,sp,144
	jr	ra
	.size	getString, .-getString
	.align	2
	.globl	toString
	.type	toString, @function
toString:
	addi	sp,sp,-96
	sw	s3,76(sp)
	sw	ra,92(sp)
	sw	s0,88(sp)
	sw	s1,84(sp)
	sw	s2,80(sp)
	li	s3,0
	bge	a0,zero,.L25
	neg	a0,a0
	li	s3,1
.L25:
	mv	s2,sp
	mv	s1,s2
	li	a4,10
.L26:
	rem	s0,a0,a4
	addi	s1,s1,1
	div	a0,a0,a4
	andi	s0,s0,0xff
	sb	s0,-1(s1)
	bne	a0,zero,.L26
	li	a0,64
	call	malloc
	sub	a4,s1,s2
	add	a4,a4,s3
	sw	a4,0(a0)
	mv	a5,a0
	addi	a0,a0,4
	beq	s3,zero,.L27
	li	a4,45
	sb	a4,4(a5)
.L27:
	beq	s1,s2,.L24
	addi	s3,s3,4
	add	a5,a5,s3
	j	.L29
.L37:
	lbu	s0,-1(s1)
.L29:
	addi	s0,s0,48
	sb	s0,0(a5)
	addi	s1,s1,-1
	addi	a5,a5,1
	bne	s1,s2,.L37
.L24:
	lw	ra,92(sp)
	lw	s0,88(sp)
	lw	s1,84(sp)
	lw	s2,80(sp)
	lw	s3,76(sp)
	addi	sp,sp,96
	jr	ra
	.size	toString, .-toString
	.align	2
	.globl	_string_substring
	.type	_string_substring, @function
_string_substring:
	addi	sp,sp,-32
	sw	s3,12(sp)
	sub	s3,a2,a1
	sw	s1,20(sp)
	mv	s1,a0
	addi	a0,s3,4
	sw	s0,24(sp)
	sw	s2,16(sp)
	sw	ra,28(sp)
	mv	s0,a1
	mv	s2,a2
	call	malloc
	sw	s3,0(a0)
	addi	a0,a0,4
	ble	s2,s0,.L38
	add	a1,s1,s0
	mv	a5,a0
	add	a2,s1,s2
.L40:
	lbu	a4,0(a1)
	addi	a1,a1,1
	addi	a5,a5,1
	sb	a4,-1(a5)
	bne	a1,a2,.L40
.L38:
	lw	ra,28(sp)
	lw	s0,24(sp)
	lw	s1,20(sp)
	lw	s2,16(sp)
	lw	s3,12(sp)
	addi	sp,sp,32
	jr	ra
	.size	_string_substring, .-_string_substring
	.align	2
	.globl	_string_parseInt
	.type	_string_parseInt, @function
_string_parseInt:
	lbu	a2,0(a0)
	li	a4,9
	mv	a3,a0
	addi	a5,a2,-48
	andi	a5,a5,0xff
	li	a0,0
	bgtu	a5,a4,.L46
	li	a1,9
.L45:
	slli	a5,a0,2
	add	a5,a5,a0
	addi	a3,a3,1
	slli	a5,a5,1
	add	a5,a5,a2
	lbu	a2,0(a3)
	addi	a0,a5,-48
	addi	a4,a2,-48
	andi	a4,a4,0xff
	bleu	a4,a1,.L45
	ret
.L46:
	ret
	.size	_string_parseInt, .-_string_parseInt
	.align	2
	.globl	_string_ord
	.type	_string_ord, @function
_string_ord:
	add	a0,a0,a1
	lbu	a0,0(a0)
	ret
	.size	_string_ord, .-_string_ord
	.align	2
	.globl	_string_add
	.type	_string_add, @function
_string_add:
	addi	sp,sp,-32
	sw	s1,20(sp)
	sw	s3,12(sp)
	lw	s1,-4(a0)
	lw	s3,-4(a1)
	sw	s4,8(sp)
	mv	s4,a0
	add	s3,s1,s3
	addi	a0,s3,4
	sw	ra,28(sp)
	sw	s0,24(sp)
	sw	s2,16(sp)
	sw	s5,4(sp)
	mv	s2,a1
	call	malloc
	addi	s5,a0,4
	mv	s0,a0
	mv	a1,s4
	mv	a0,s5
	sw	s3,0(s0)
	call	strcpy
	addi	a0,s1,4
	mv	a1,s2
	add	a0,s0,a0
	call	strcpy
	lw	ra,28(sp)
	lw	s0,24(sp)
	lw	s1,20(sp)
	lw	s2,16(sp)
	lw	s3,12(sp)
	lw	s4,8(sp)
	mv	a0,s5
	lw	s5,4(sp)
	addi	sp,sp,32
	jr	ra
	.size	_string_add, .-_string_add
	.ident	"GCC: (GNU) 9.2.0"
	.section	.note.GNU-stack,"",@progbits
