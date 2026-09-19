/**
 * EAN-13 encoder, mirroring `computer-vision/labvision/ean13.py`.
 *
 * The wrist-camera view draws the label of the container the robot is looking
 * at, and it draws the real bars for the real code from the sample registry.
 * Only encoding is needed here; decoding lives in the perception pipeline.
 */

const L_CODES = [
  '0001101', '0011001', '0010011', '0111101', '0100011',
  '0110001', '0101111', '0111011', '0110111', '0001011',
]
const G_CODES = [
  '0100111', '0110011', '0011011', '0100001', '0011101',
  '0111001', '0000101', '0010001', '0001001', '0010111',
]
const R_CODES = [
  '1110010', '1100110', '1101100', '1000010', '1011100',
  '1001110', '1010000', '1000100', '1001000', '1110100',
]
/** Parity of the six left-hand digits, selected by the first digit. */
const PARITY = [
  '000000', '001011', '001101', '001110', '010011',
  '011001', '011100', '010101', '010110', '011010',
]

const START_GUARD = '101'
const CENTRE_GUARD = '01010'
const END_GUARD = '101'

/** Total module count of an EAN-13 symbol, excluding quiet zones. */
export const MODULES_PER_SYMBOL = 95

/** Compute the check digit of a 12-digit payload. */
export function checkDigit(payload: string): number {
  let sum = 0
  for (let i = 0; i < 12; i++) {
    const d = Number(payload[i])
    sum += i % 2 === 0 ? d : d * 3
  }
  return (10 - (sum % 10)) % 10
}

/** True when `code` is 13 digits whose check digit is correct. */
export function isValid(code: string): boolean {
  return /^\d{13}$/.test(code) && checkDigit(code.slice(0, 12)) === Number(code[12])
}

/**
 * Encode a 13-digit code as its 95-module bar pattern.
 *
 * Returns a string of "0" (space) and "1" (bar). An invalid code is still
 * encoded, so a wrong label can be drawn; callers check `isValid` if they care.
 */
export function encodeModules(code: string): string {
  const digits = code.padEnd(13, '0').slice(0, 13)
  const parity = PARITY[Number(digits[0])] ?? PARITY[0]
  let left = ''
  for (let i = 0; i < 6; i++) {
    const d = Number(digits[i + 1])
    left += (parity[i] === '1' ? G_CODES : L_CODES)[d]
  }
  let right = ''
  for (let i = 7; i < 13; i++) right += R_CODES[Number(digits[i])]
  return START_GUARD + left + CENTRE_GUARD + right + END_GUARD
}
