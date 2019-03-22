PROGRAM Matrix_mult

  INTEGER, PARAMETER :: num = KIND(1.0)
  INTEGER, PARAMETER :: nels = 2000
  REAL(num), DIMENSION(:,:), ALLOCATABLE :: mat1, mat2, mat3
  INTEGER :: seed

  seed = 10000

  ALLOCATE(mat1(nels, nels), mat2(nels,nels), mat3(nels, nels))
  CALL RANDOM_SEED(seed)
  CALL RANDOM_NUMBER(mat1)
  CALL RANDOM_NUMBER(mat2)

  PRINT *,'Generated matrix'

  mat3 = MATMUL(mat1, mat2)

  PRINT *, MAXVAL(mat3)

END PROGRAM matrix_mult
