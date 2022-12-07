.data
	var_a:  .word  0:1
.text
main:

	li $a0, 3

	sw $a0 0($sp)
	add $sp $sp -4

	li $a0, 3

	lw $t1 4($sp)
	sub $a0 $t1 $a0
	add $sp $sp 4

	sw $a0 0($sp)
	add $sp $sp -4

	li $a0, 1

	lw $t1 4($sp)
	add $a0 $t1 $a0
	add $sp $sp 4

	la $t0, var_a
	sw $a0, 0($t0)

	jr $ra