	.file	"builtin.c"
	.option nopic
	.text
	.align	2
	.globl	print
	.type	print, @function
print:
	addi	sp,sp,-48
	sw	ra,44(sp)
	sw	s0,40(sp)
	addi	s0,sp,48
	sw	a0,-36(s0)
	lw	a5,-36(s0)
	lw	a5,-4(a5)
	sw	a5,-24(s0)
	sw	zero,-20(s0)
	j	.L2
.L3:
	lw	a5,-20(s0)
	lw	a4,-36(s0)
	add	a5,a4,a5
	lbu	a5,0(a5)
	mv	a0,a5
	call	putchar
	lw	a5,-20(s0)
	addi	a5,a5,1
	sw	a5,-20(s0)
.L2:
	lw	a4,-20(s0)
	lw	a5,-24(s0)
	blt	a4,a5,.L3
	nop
	nop
	lw	ra,44(sp)
	lw	s0,40(sp)
	addi	sp,sp,48
	jr	ra
	.size	print, .-print
	.align	2
	.globl	println
	.type	println, @function
println:
	addi	sp,sp,-32
	sw	ra,28(sp)
	sw	s0,24(sp)
	addi	s0,sp,32
	sw	a0,-20(s0)
	lw	a0,-20(s0)
	call	print
	li	a0,10
	call	putchar
	nop
	lw	ra,28(sp)
	lw	s0,24(sp)
	addi	sp,sp,32
	jr	ra
	.size	println, .-println
	.section	.rodata
	.align	2
.LC0:
	.string	"%d"
	.text
	.align	2
	.globl	printInt
	.type	printInt, @function
printInt:
	addi	sp,sp,-32
	sw	ra,28(sp)
	sw	s0,24(sp)
	addi	s0,sp,32
	sw	a0,-20(s0)
	lw	a1,-20(s0)
	lui	a5,%hi(.LC0)
	addi	a0,a5,%lo(.LC0)
	call	printf
	nop
	lw	ra,28(sp)
	lw	s0,24(sp)
	addi	sp,sp,32
	jr	ra
	.size	printInt, .-printInt
	.align	2
	.globl	printlnInt
	.type	printlnInt, @function
printlnInt:
	addi	sp,sp,-32
	sw	ra,28(sp)
	sw	s0,24(sp)
	addi	s0,sp,32
	sw	a0,-20(s0)
	lw	a0,-20(s0)
	call	printInt
	li	a0,10
	call	putchar
	nop
	lw	ra,28(sp)
	lw	s0,24(sp)
	addi	sp,sp,32
	jr	ra
	.size	printlnInt, .-printlnInt
	.align	2
	.globl	getInt
	.type	getInt, @function
getInt:
	addi	sp,sp,-32
	sw	ra,28(sp)
	sw	s0,24(sp)
	addi	s0,sp,32
	sw	zero,-20(s0)
	addi	a5,s0,-20
	mv	a1,a5
	lui	a5,%hi(.LC0)
	addi	a0,a5,%lo(.LC0)
	call	__isoc99_scanf
	lw	a5,-20(s0)
	mv	a0,a5
	lw	ra,28(sp)
	lw	s0,24(sp)
	addi	sp,sp,32
	jr	ra
	.size	getInt, .-getInt
	.section	.rodata
	.align	2
.LC1:
	.string	"%s"
	.text
	.align	2
	.globl	getString
	.type	getString, @function
getString:
	addi	sp,sp,-160
	sw	ra,156(sp)
	sw	s0,152(sp)
	addi	s0,sp,160
	addi	a5,s0,-152
	mv	a1,a5
	lui	a5,%hi(.LC1)
	addi	a0,a5,%lo(.LC1)
	call	__isoc99_scanf
	addi	a5,s0,-152
	mv	a0,a5
	call	strlen
	mv	a5,a0
	sw	a5,-20(s0)
	lw	a5,-20(s0)
	addi	a5,a5,4
	mv	a0,a5
	call	malloc
	mv	a5,a0
	sw	a5,-24(s0)
	lw	a5,-24(s0)
	lw	a4,-20(s0)
	sw	a4,0(a5)
	lw	a5,-24(s0)
	addi	a5,a5,4
	addi	a4,s0,-152
	mv	a1,a4
	mv	a0,a5
	call	strcpy
	lw	a5,-24(s0)
	addi	a5,a5,4
	mv	a0,a5
	lw	ra,156(sp)
	lw	s0,152(sp)
	addi	sp,sp,160
	jr	ra
	.size	getString, .-getString
	.align	2
	.globl	toString
	.type	toString, @function
toString:
	addi	sp,sp,-112
	sw	ra,108(sp)
	sw	s0,104(sp)
	addi	s0,sp,112
	sw	a0,-100(s0)
	addi	a5,s0,-96
	sw	a5,-20(s0)
	sw	zero,-24(s0)
	lw	a5,-100(s0)
	bge	a5,zero,.L13
	li	a5,1
	sw	a5,-24(s0)
	lw	a5,-100(s0)
	neg	a5,a5
	sw	a5,-100(s0)
.L13:
	lw	a4,-100(s0)
	li	a5,10
	rem	a3,a4,a5
	lw	a5,-20(s0)
	addi	a4,a5,1
	sw	a4,-20(s0)
	andi	a4,a3,0xff
	sb	a4,0(a5)
	lw	a4,-100(s0)
	li	a5,10
	div	a5,a4,a5
	sw	a5,-100(s0)
	lw	a5,-100(s0)
	bne	a5,zero,.L13
	li	a0,64
	call	malloc
	mv	a5,a0
	sw	a5,-32(s0)
	addi	a5,s0,-96
	lw	a4,-20(s0)
	sub	a4,a4,a5
	lw	a5,-24(s0)
	add	a4,a4,a5
	lw	a5,-32(s0)
	sw	a4,0(a5)
	lw	a5,-32(s0)
	addi	a5,a5,4
	sw	a5,-32(s0)
	lw	a5,-24(s0)
	beq	a5,zero,.L14
	lw	a5,-32(s0)
	li	a4,45
	sb	a4,0(a5)
.L14:
	sw	zero,-28(s0)
	j	.L15
.L16:
	lw	a5,-20(s0)
	addi	a5,a5,-1
	sw	a5,-20(s0)
	lw	a5,-20(s0)
	lbu	a4,0(a5)
	lw	a3,-28(s0)
	lw	a5,-24(s0)
	add	a5,a3,a5
	mv	a3,a5
	lw	a5,-32(s0)
	add	a5,a5,a3
	addi	a4,a4,48
	andi	a4,a4,0xff
	sb	a4,0(a5)
	lw	a5,-28(s0)
	addi	a5,a5,1
	sw	a5,-28(s0)
.L15:
	addi	a5,s0,-96
	lw	a4,-20(s0)
	bne	a4,a5,.L16
	lw	a5,-32(s0)
	mv	a0,a5
	lw	ra,108(sp)
	lw	s0,104(sp)
	addi	sp,sp,112
	jr	ra
	.size	toString, .-toString
	.align	2
	.globl	_string_substring
	.type	_string_substring, @function
_string_substring:
	addi	sp,sp,-48
	sw	ra,44(sp)
	sw	s0,40(sp)
	addi	s0,sp,48
	sw	a0,-36(s0)
	sw	a1,-40(s0)
	sw	a2,-44(s0)
	lw	a4,-44(s0)
	lw	a5,-40(s0)
	sub	a5,a4,a5
	addi	a5,a5,4
	mv	a0,a5
	call	malloc
	mv	a5,a0
	sw	a5,-24(s0)
	lw	a4,-44(s0)
	lw	a5,-40(s0)
	sub	a4,a4,a5
	lw	a5,-24(s0)
	sw	a4,0(a5)
	lw	a5,-24(s0)
	addi	a5,a5,4
	sw	a5,-24(s0)
	lw	a5,-40(s0)
	sw	a5,-20(s0)
	j	.L19
.L20:
	lw	a5,-20(s0)
	lw	a4,-36(s0)
	add	a4,a4,a5
	lw	a3,-20(s0)
	lw	a5,-40(s0)
	sub	a5,a3,a5
	mv	a3,a5
	lw	a5,-24(s0)
	add	a5,a5,a3
	lbu	a4,0(a4)
	sb	a4,0(a5)
	lw	a5,-20(s0)
	addi	a5,a5,1
	sw	a5,-20(s0)
.L19:
	lw	a4,-20(s0)
	lw	a5,-44(s0)
	blt	a4,a5,.L20
	lw	a5,-24(s0)
	mv	a0,a5
	lw	ra,44(sp)
	lw	s0,40(sp)
	addi	sp,sp,48
	jr	ra
	.size	_string_substring, .-_string_substring
	.align	2
	.globl	_string_parseInt
	.type	_string_parseInt, @function
_string_parseInt:
	addi	sp,sp,-48
	sw	s0,44(sp)
	addi	s0,sp,48
	sw	a0,-36(s0)
	sw	zero,-20(s0)
	j	.L23
.L25:
	lw	a4,-20(s0)
	mv	a5,a4
	slli	a5,a5,2
	add	a5,a5,a4
	slli	a5,a5,1
	mv	a3,a5
	lw	a5,-36(s0)
	addi	a4,a5,1
	sw	a4,-36(s0)
	lbu	a5,0(a5)
	add	a5,a3,a5
	addi	a5,a5,-48
	sw	a5,-20(s0)
.L23:
	lw	a5,-36(s0)
	lbu	a4,0(a5)
	li	a5,47
	bleu	a4,a5,.L24
	lw	a5,-36(s0)
	lbu	a4,0(a5)
	li	a5,57
	bleu	a4,a5,.L25
.L24:
	lw	a5,-20(s0)
	mv	a0,a5
	lw	s0,44(sp)
	addi	sp,sp,48
	jr	ra
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
