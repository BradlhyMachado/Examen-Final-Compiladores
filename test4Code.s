.data
	var_b:  .word  0:1
.text
main:
	sw $fp 0($sp)
	addiu $sp $sp-4

	li $a0, 5

	sw $a0 0($sp)
	addiu $sp $sp-4

	jal fun1


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

	li $a0, 5

	lw $t1 4($sp)
	add $sp $sp 4
	beq $a0 $t1 label_true1

label_false1:

	li $a0, 10

	sw $a0 0($sp)
	add $sp $sp -4

	li $a0, 3

	lw $t1 4($sp)
	sub $a0 $t1 $a0
	add $sp $sp 4

	la $t0, var_b
	sw $a0, 0($t0)

	b label_end1

label_true1:

	lw $a0, 8($sp)

	sw $a0 0($sp)
	add $sp $sp -4

	li $a0, 8

	lw $t1 4($sp)
	add $a0 $t1 $a0
	add $sp $sp 4

	sw $a0 0($sp)
	add $sp $sp -4

	li $a0, 3

	lw $t1 4($sp)
	sub $a0 $t1 $a0
	add $sp $sp 4

	la $t0, var_b
	sw $a0, 0($t0)

label_end1:

	la $t0, var_b
	lw $a0, 0($t0)

	sw $a0 0($sp)
	add $sp $sp -4

	li $a0, 10

	lw $t1 4($sp)
	add $sp $sp 4
	beq $a0 $t1 label_true2

label_false2:

	li $a0, 100

	la $t0, var_b
	sw $a0, 0($t0)

	b label_end2

label_true2:

	li $a0, 0

	la $t0, var_b
	sw $a0, 0($t0)

label_end2:
	lw $ra 4($sp)
	addiu $sp $sp 12
	lw $fp 0($sp)

	jr $ra