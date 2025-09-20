import { SongStatus, GenerationType } from "../domain/song";
import type { Song } from "../domain/song";
import type { AudioParameters } from "../domain/song";

export interface SongRepository {
  create(song: Omit<Song, "id" | "createdAt" | "updatedAt">): Promise<Song>;
  findById(id: string): Promise<Song | null>;
  updateStatus(id: string, status: SongStatus): Promise<Song>;
  updateWithAudioData(
    id: string,
    audioR2Key: string,
    coverImageR2Key: string,
    categories: string[],
  ): Promise<Song>;
}

export interface QueueService {
  queueSong(songId: string, data: any): Promise<void>;
}

export interface StorageService {
  getPresignedUrl(key: string): Promise<string>;
}

export interface MusicGenerationRequest {
  generationType: GenerationType;
  prompt?: string;
  lyrics?: string;
  describedLyrics?: string;
  fullDescribedSong?: string;
  audioParameters: AudioParameters;
}

export interface MusicGenerationResponse {
  r2key: string;
  coverImageR2Key: string;
  categories: string[];
}

export interface AIService {
  generateMusic(
    request: MusicGenerationRequest,
  ): Promise<MusicGenerationResponse>;
}
