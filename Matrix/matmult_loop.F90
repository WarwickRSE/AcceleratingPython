

PROGRAM main

  IMPLICIT NONE

  INTEGER :: i, j, k

  DOUBLE PRECISION, DIMENSION(:,:), ALLOCATABLE :: A, B, C
  INTEGER :: seed, start_time, stop_time
  INTEGER, PARAMETER :: length = 5000

  ALLOCATE(A(length,length), B(length, length), C(length, length))

  seed = 13983
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

