PROGRAM main

  IMPLICIT NONE

  CHARACTER(LEN=32) :: arg
  INTEGER :: i, j, k
  INTEGER :: length = 5000
  DOUBLE PRECISION, DIMENSION(:,:), ALLOCATABLE :: A, B, C
  INTEGER :: seed, start_time, stop_time

  IF (COMMAND_ARGUMENT_COUNT() == 1) THEN
    CALL GET_COMMAND_ARGUMENT(1, arg)
    READ(arg,*) length
  END IF

  ALLOCATE(A(length,length), B(length, length), C(length, length))

  seed = 10000

  PRINT *, 'Multipliying ', length, ' square matrices'

  CALL RANDOM_SEED(seed)
  CALL RANDOM_NUMBER(A)
  CALL RANDOM_NUMBER(B)

  !Pretend B is transposed to get nicer ordering
  CALL SYSTEM_CLOCK(start_time)

  DO i = 1, length
    DO j = 1, length
      DO k = 1, length
        C(j, i) = A(k, j) * B(k, i)
      END DO
    END DO
  END DO

  CALL SYSTEM_CLOCK(stop_time)

  PRINT *,'Time in ms ',stop_time-start_time
  !Need this to avoid compiler optimising out whole operation
  PRINT *,'Max of result ', MAXVAL(C)

END PROGRAM

