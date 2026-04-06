

# COMP128 card key extraction simulator
> This is a simulator that attempts to extract the secret key (ki) from the COMP128 algorithm, we'll first define the algorithm, what it produces, how it's used to authenticate the SIM card, how it was compromised and lastly how <strong> we </strong> will do so.


## COMP128-1
 There are several versions to this algorithm or hash function, the one we'll attack is the <b>-1</b> version, it holds a secret key (key identifier), and when the network tries to reach it and verify the SIM's authenticity, it sends a challenge (SRAND), and the algorithm would produce a response (SRES). Below is the structured detail on how COMP128-1 works:
  1.SIM sends out IMSI (unique user identifier) to AuC (Authentication Center) to verify the Ki (indexed by IMSI)
  2.The AuC sends a challenge (SRAND) to SIM as a 16 byte data.
  3.The SIM concatenate the SRAND with Ki (which is also 16-byte sized) and begins the eight round iteration.
  4.The SIM produces the output (SRES, KC) and sends out the SRES to Auc.
  5.AuC compares its SRES to the ones the SIM sent, reject if not identical, else continue to step 6.
  6.An encrypted session begins between AuC and SIM under the KC key.


### Compression process:
 The most important, and ironically flawed process is the compression, it goes through 5 round per round from the 8 rounds in step 3. each rounds diassambles the state (SRAND,KI) into four nibbles `(SRAND_HIGH, SRAND_LOW. KI_HI, KI_LOW)`, XORs the nibbles respective to their position (HIGH XOR HIGH, LOW XOR LOW), look up the corresponded value from the <b>Transposition table</b>, reducing the length to half. Because it takes 5 rounds, the 32 byte initial state becomes 1-byte sized.
 The Flaw is how the Transposition table was built, having too many repeated values inside it. Different inputs have the same output.
 `T[0xF][0xF] = 0x0E`
  `T[0xF][0xE] = 0x0E`
  `T[0xE][0xF] = 0x0E`
  `T[0xD][0xD] = 0x0E`

While it may look useful to destroy any patterns, it vastly increases the possibility of collision (two different inputs making the same output), hence cutting down the group Ki can be in.
`RAND_A XOR Ki  →  T[0xF][0xF] = 0x0E`
`RAND_B XOR Ki  →  T[0xF][0xE] = 0x0E ← same result`

### FormBitsFromBytes process:
 This is a simple procedure where the final 1-byte sized result's bits are rearrenged with a fixed reorderer, further increasing the randomness.

### Shuffle Process:
 This permutes the position of bytes before the second supround so that compression doesn't hit the same byte pairs.


## Implementation:
 To simulate this attack we'll start with hardcoding the fixed stuff, those are <strong> The transposition table </strong> and <strong> The reorderer </strong> and <strong> The permutation pattern </strong>.
 Then, we'll implement the COMP128-1, then the SIM Card to make it run all SRANDs fast, then the attack.
 For the sake of simplicity and speed, we'll reduce the data sizes.*
 **Key size: 128 bits → 16 bits** The real Ki and RAND are 128 bits (16 bytes)
 **S-box size: 512 entries → 16 entries**
 **Rounds: 8 → 4**
 

