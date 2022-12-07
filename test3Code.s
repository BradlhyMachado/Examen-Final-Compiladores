.data
	var_y:  .word  0:1
	var_x:  .word  0:1
.text
main:
	sw $fp 0($sp)
	addiu $sp $sp-4

	li $a0, 8

	sw $a0 0($sp)
	addiu $sp $sp-4

	li $a0, 9

	sw $a0 0($sp)
	addiu $sp $sp-4

	jal fun1

	la $t0, var_x
	sw $a0, 0($t0)

	li $v0, 1
	syscall

	li $v0, 10
	syscall

fun1:
	move $fp $sp
	sw $ra 0($sp)
	addiu $sp $sp -4

	lw $a0, 8($sp)

	sw $a0 0($sp)
	add $sp $sp -4

	lw $a0, 16($sp)

	lw $t1 4($sp)
	add $a0 $t1 $a0
	add $sp $sp 4

	sw $a0 0($sp)
	add $sp $sp -4

	li $a0, 2

	lw $t1 4($sp)
	add $a0 $t1 $a0
	add $sp $sp 4

	la $t0, var_y
	sw $a0, 0($t0)
	lw $ra 4($sp)
	addiu $sp $sp 16
	lw $fp 0($sp)

	jr $ra