from dataclasses import dataclass
from functools import cache, cached_property
from pathlib import Path

from pydub import AudioSegment

from voice import VOICE_DIR, Voice, get_durations


@dataclass(frozen=True, kw_only=True)
class BreatheConfig:
    breathe_in: int = 4
    hold_in: int = 4
    breathe_out: int = 4
    hold_out: int = 4
    voice: Voice = Voice.af

    def _add_step(
        self,
        base_audio: AudioSegment,
        folder: Path,
        filename: str,
        target_sec: int,
        actual_sec: float,
    ) -> AudioSegment:
        step_audio = AudioSegment.from_wav(folder / f"{filename}.wav")
        silence_ms = max(0, (target_sec - actual_sec) * 1000)
        return base_audio + step_audio + AudioSegment.silent(duration=silence_ms)

    def generate_round_audio(self, short: bool = False) -> AudioSegment:
        durations = get_durations(self.voice)
        voice_path = Path(VOICE_DIR) / self.voice
        audio = AudioSegment.empty()

        suffix = "_short" if short else ""
        audio = self._add_step(
            audio,
            voice_path,
            f"in{suffix}",
            self.breathe_in,
            durations.breathe_in_short if short else durations.breathe_in,
        )

        if self.hold_in > 0:
            audio = self._add_step(
                audio, voice_path, "hold", self.hold_in, durations.hold
            )

        audio = self._add_step(
            audio,
            voice_path,
            f"out{suffix}",
            self.breathe_out,
            durations.breathe_out_short if short else durations.breathe_out,
        )

        if self.hold_out > 0:
            audio = self._add_step(
                audio, voice_path, "hold", self.hold_out, durations.hold
            )

        return audio

    @cached_property
    def _round_audio(self) -> AudioSegment:
        return self.generate_round_audio(short=False)

    @cached_property
    def _round_audio_short(self) -> AudioSegment:
        return self.generate_round_audio(short=True)

    def audio(self, rounds: int) -> AudioSegment:
        voice_path = Path(VOICE_DIR) / self.voice
        begin = AudioSegment.from_wav(voice_path / "begin.wav")

        if rounds <= 1:
            return begin + self._round_audio

        return begin + self._round_audio + (self._round_audio_short * (rounds - 1))

    @cached_property
    def round_duration(self) -> float:
        return self.breathe_in + self.breathe_out + self.hold_in + self.hold_out


@cache
def breathe_config_cache(
    *, breathe_in: int, hold_in: int, breathe_out: int, hold_out: int, voice: Voice
):
    return BreatheConfig(
        breathe_in=breathe_in,
        hold_in=hold_in,
        breathe_out=breathe_out,
        hold_out=hold_out,
        voice=voice,
    )
