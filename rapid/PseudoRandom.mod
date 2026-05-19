MODULE PseudoRandom
    ! Small deterministic pseudo-random generator.
    ! State and generated raw values are always in range 0..32767.
    ! Unit values combine two raw draws for a finer 30-bit step.

    LOCAL CONST num PRNG_MODULUS := 32768;
    LOCAL CONST num PRNG_UNIT_MODULUS := 1073741824;
    LOCAL CONST num PRNG_MAX := 32767;
    LOCAL CONST num PRNG_MULTIPLIER := 25173;
    LOCAL CONST num PRNG_INCREMENT := 13849;

    FUNC bool PrngSeedIsValid(num seed)
        RETURN seed >= 0 AND seed <= PRNG_MAX AND seed = Trunc(seed);
    ENDFUNC

    FUNC num PrngWrap(num value)
        VAR num wrapped;

        wrapped := value - PRNG_MODULUS * Trunc(value / PRNG_MODULUS);
        IF wrapped < 0 THEN
            wrapped := wrapped + PRNG_MODULUS;
        ENDIF

        RETURN wrapped;
    ENDFUNC

    PROC PrngSetSeed(INOUT num state, num seed)
        state := PrngWrap(seed);
    ENDPROC

    FUNC num PrngNext(INOUT num state)
        state := PrngWrap(PRNG_MULTIPLIER * state + PRNG_INCREMENT);
        RETURN state;
    ENDFUNC

    FUNC num PrngNextUnit(INOUT num state)
        VAR num high;
        VAR num low;

        high := PrngNext(state);
        low := PrngNext(state);
        RETURN (high * PRNG_MODULUS + low) / PRNG_UNIT_MODULUS;
    ENDFUNC

    FUNC num PrngNextRange(INOUT num state, num minimum, num maximum)
        RETURN minimum + (maximum - minimum) * PrngNextUnit(state);
    ENDFUNC

    FUNC num PrngNextInt(INOUT num state, num minimum, num maximum)
        VAR num span;

        span := maximum - minimum + 1;
        RETURN minimum + Trunc(span * PrngNextUnit(state));
    ENDFUNC
ENDMODULE
