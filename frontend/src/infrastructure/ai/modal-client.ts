import type {
  MusicGenerationRequest,
  MusicGenerationResponse,
  AIService,
} from "../../core/ports/interfaces";
import { env } from "@/env";

export class ModalAIService implements AIService {
  constructor(private bearerToken: string) {}

  async generateMusic(
    request: MusicGenerationRequest,
  ): Promise<MusicGenerationResponse> {
    const endpoint = this.getEndpoint(request.generationType);
    const payload = this.buildPayload(request);

    const response = await fetch(endpoint, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${this.bearerToken}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error("Modal AI service error:", response.status, errorText);
      throw new Error(
        `AI service error: ${response.status} ${response.statusText}`,
      );
    }

    return await response.json();
  }

  private getEndpoint(generationType: string): string {
    switch (generationType) {
      case "from_description":
        return env.GENERATE_FROM_DESCRIPTION;
      case "with_custom_lyrics":
        return env.GENERATE_WITH_LYRICS;
      case "with_described_lyrics":
        return env.GENERATE_FROM_DESCRIBED_LYRICS;
      default:
        throw new Error(`Unknown generation type: ${generationType}`);
    }
  }

  private buildPayload(request: MusicGenerationRequest): any {
    const base = {
      audio_duration: request.audioParameters.audioDuration,
      seed: request.audioParameters.seed,
      guidance_scale: request.audioParameters.guidanceScale,
      infer_step: request.audioParameters.inferStep,
      instrumental: request.audioParameters.instrumental,
    };

    switch (request.generationType) {
      case "from_description":
        return {
          ...base,
          full_described_song: request.fullDescribedSong,
        };
      case "with_custom_lyrics":
        return {
          ...base,
          prompt: request.prompt,
          lyrics: request.lyrics,
        };
      case "with_described_lyrics":
        return {
          ...base,
          prompt: request.prompt,
          described_lyrics: request.describedLyrics,
        };
      default:
        throw new Error(`Unknown generation type: ${request.generationType}`);
    }
  }
}
