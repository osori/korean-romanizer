"""
Context-sensitive pronunciation substitutions before romanization.

The Pronouncer applies Korean sandhi (phonological change) rules to
produce the actual pronunciation of a text. These rules modify
syllable-final consonants based on what follows them.
"""
from korean_romanizer.syllable import Syllable
from korean_romanizer.tables import (
    ASPIRATION_MAP,
    DOUBLE_CONSONANT_FINAL,
    NULL_CONSONANT,
    REPRESENTATIVE_SOUND,
    WITHOUT_H_FINAL,
)


class Pronouncer(object):
    def __init__(self, text):
        self._syllables = [Syllable(char) for char in text]
        self._apply_pronunciation_rules()
        self.pronounced = ''.join(str(c) for c in self._syllables)

    def _apply_pronunciation_rules(self):
        """Apply all pronunciation sandhi rules to the syllable sequence."""
        for idx, syllable in enumerate(self._syllables):
            next_syllable = self._get_next_syllable(idx)
            context = self._determine_context(syllable, next_syllable)
            self._apply_representative_sound(syllable, context)
            self._apply_h_rules(syllable, next_syllable)
            self._apply_double_consonant_linking(syllable, next_syllable)
            self._apply_single_consonant_linking(syllable, next_syllable, context)

    def _get_next_syllable(self, idx):
        """Get the next syllable in the sequence, or None if at the end."""
        try:
            return self._syllables[idx + 1]
        except IndexError:
            return None

    def _determine_context(self, syllable, next_syllable):
        """Determine the phonological context of a syllable's final consonant."""
        try:
            final_is_before_C = syllable.final and next_syllable.initial not in (None, NULL_CONSONANT)
        except AttributeError:
            final_is_before_C = False

        try:
            final_is_before_V = syllable.final and next_syllable.initial in (None, NULL_CONSONANT)
        except AttributeError:
            final_is_before_V = False

        is_last_syllable = syllable.final and next_syllable is None

        return {
            'final_is_before_C': final_is_before_C,
            'final_is_before_V': final_is_before_V,
            'is_last_syllable': is_last_syllable,
        }

    def _apply_representative_sound(self, syllable, context):
        """Rules 1-3: Reduce complex codas to their representative sound at
        word-final position or before another consonant."""
        if context['is_last_syllable'] or context['final_is_before_C']:
            if syllable.final in REPRESENTATIVE_SOUND:
                syllable.final = REPRESENTATIVE_SOUND[syllable.final]

    def _apply_h_rules(self, syllable, next_syllable):
        """Rule 4: Handle the pronunciation of ㅎ (hiut) in coda position."""
        if syllable.final not in ('ᇂ', 'ᆭ', 'ᆶ'):
            return

        if next_syllable:
            # 'ㅎ(ㄶ, ㅀ)' + ㄱ/ㄷ/ㅈ/ㅅ → aspirate the following consonant
            if next_syllable.initial in ASPIRATION_MAP:
                syllable.final = WITHOUT_H_FINAL[syllable.final]
                next_syllable.initial = ASPIRATION_MAP[next_syllable.initial]
            # 'ㅎ' + ㄴ → [ㄴ]
            elif next_syllable.initial == 'ᄂ':
                # [붙임] 'ㄶ, ㅀ' + ㄴ → 'ㅎ' not pronounced
                if syllable.final in ('ᆭ', 'ᆶ'):
                    syllable.final = WITHOUT_H_FINAL[syllable.final]
                else:
                    syllable.final = 'ᆫ'
            # 'ㅎ(ㄶ, ㅀ)' + vowel → 'ㅎ' not pronounced
            elif next_syllable.initial == NULL_CONSONANT:
                if syllable.final in ('ᆭ', 'ᆶ'):
                    syllable.final = 'ᆫ' if syllable.final == 'ᆭ' else 'ᆯ'
                else:
                    syllable.final = None
            # 'ㅀ' + ㄹ → ㄹ
            elif next_syllable.initial == 'ᄅ':
                if syllable.final == 'ᆶ':
                    syllable.final = 'ᆯ'
            else:
                if syllable.final == 'ᇂ':
                    syllable.final = None
        else:
            # Word-final: strip the ㅎ
            syllable.final = WITHOUT_H_FINAL[syllable.final]

    def _apply_double_consonant_linking(self, syllable, next_syllable):
        """Rule 6: Double consonant final before vowel — move second element
        to next syllable's onset."""
        if (syllable.final in DOUBLE_CONSONANT_FINAL
                and next_syllable is not None
                and next_syllable.initial == NULL_CONSONANT):
            double_consonant = DOUBLE_CONSONANT_FINAL[syllable.final]
            syllable.final = double_consonant[0]
            next_syllable.initial = next_syllable.final_to_initial(double_consonant[1])

    def _apply_single_consonant_linking(self, syllable, next_syllable, context):
        """Rule 5: Single or double consonant before vowel — move final to
        next syllable's onset (unless it's ᆼ or null)."""
        if (next_syllable is not None
                and context['final_is_before_V']
                and next_syllable.initial == NULL_CONSONANT
                and syllable.final not in ("ᆼ", None)):
            next_syllable.initial = next_syllable.final_to_initial(syllable.final)
            syllable.final = None
