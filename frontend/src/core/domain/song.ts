export enum SongStatus {
  QUEUED = "queued",
  PROCESSING = "processing",
  COMPLETED = "completed",
  FAILED = "failed",
}

export enum GenerationType {
  FROM_DESCRIPTION = "from_description",
  WITH_CUSTOM_LYRICS = "with_custom_lyrics",
  WITH_DESCRIBED_LYRICS = "with_described_lyrics",
}

export interface Song {
  id: string;
  status: SongStatus;
  generationType: GenerationType;
  prompt?: string;
  lyrics?: string;
  describedLyrics?: string;
  fullDescribedSong?: string;
  audioR2Key?: string;
  coverImageR2Key?: string;
  categories: string[];
  userId: string;
  audioParameters: AudioParameters;
  createdAt: Date;
  updatedAt: Date;
}

export interface AudioParameters {
  audioDuration: number;
  seed: number;
  guidanceScale: number;
  inferStep: number;
  instrumental: boolean;
}

export class AudioParametersVO {
  constructor(
    public readonly audioDuration: number = 180.0,
    public readonly seed: number = -1,
    public readonly guidanceScale: number = 15.0,
    public readonly inferStep: number = 60,
    public readonly instrumental: boolean = false,
  ) {}

  static fromObject(obj: Partial<AudioParameters>): AudioParametersVO {
    return new AudioParametersVO(
      obj.audioDuration,
      obj.seed,
      obj.guidanceScale,
      obj.inferStep,
      obj.instrumental,
    );
  }
}
