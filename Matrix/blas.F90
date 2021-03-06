PROGRAM Matrix_mult

  INTEGER, PARAMETER :: num = KIND(1.D0)
  CHARACTER(LEN=32) :: arg
  INTEGER :: nels = 5000
  REAL(num), DIMENSION(:,:), ALLOCATABLE :: mat1, mat2, mat3
  INTEGER :: start_time, stop_time
  INTEGER :: seed

  IF (COMMAND_ARGUMENT_COUNT() == 1) THEN
    CALL GET_COMMAND_ARGUMENT(1, arg)
    READ(arg,*) nels
  END IF

  seed = 10000

  PRINT *, 'Multipliying ', nels, ' square matrices'

  ALLOCATE(mat1(nels, nels), mat2(nels,nels), mat3(nels, nels))
  CALL RANDOM_SEED(seed)
  CALL RANDOM_NUMBER(mat1)
  CALL RANDOM_NUMBER(mat2)
  mat3 = 0.0_num

  CALL SYSTEM_CLOCK(start_time)
  CALL DGEMM('n','n', nels, nels, nels, 1.0_num, mat1, nels, mat2, nels, &
      0.0_num, mat3, nels)
  CALL SYSTEM_CLOCK(stop_time)

  PRINT *,'Time in ms ',stop_time-start_time
  !Need this to avoid compiler optimising out whole operation
  PRINT *,'Max of result ', MAXVAL(mat3)

END PROGRAM matrix_mult
