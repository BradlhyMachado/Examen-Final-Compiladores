.data
	var_a:  .word  0:1
	var_y:  .word  0:1
.text
main:

	li $a0, 5

	sw $a0 0($sp)
	add $sp $sp -4

	li $a0, 6

	lw $t1 4($sp)
	add $a0 $t1 $a0
	add $sp $sp 4

	la $t0, var_a
	sw $a0, 0($t0)

	la $t0, var_a
	lw $a0, 0($t0)

	sw $a0 0($sp)
	addiu $sp $sp -4

	la $t0, var_a
	lw $a0, 0($t0)

	lw $t1 4($sp)
	add $a0 $t1 $a0
	add $sp $sp 4

	la $t0, var_y
	sw $a0, 0($t0)

	li $v0, 1
	syscall

	jr $ra