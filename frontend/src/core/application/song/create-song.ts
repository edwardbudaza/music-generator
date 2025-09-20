import { PrismaClient } from "@prisma/client";
import { SongStatus } from "../../../core/domain/song";
import type { Song } from "../../../core/domain/song";
import type { SongRepository } from "../../../core/ports/interfaces";

export class PrismaSongRepository implements SongRepository {
  constructor(private prisma: PrismaClient) {}

  async create(
    songData: Omit<Song, "id" | "createdAt" | "updatedAt">,
  ): Promise<Song> {
    const result = await this.prisma.song.create({
      data: {
        status: songData.status,
        generationType: songData.generationType,
        prompt: songData.prompt,
        lyrics: songData.lyrics,
        describedLyrics: songData.describedLyrics,
        fullDescribedSong: songData.fullDescribedSong,
        audioR2Key: songData.audioR2Key,
        coverImageR2Key: songData.coverImageR2Key,
        // Fix: Use proper Prisma relation syntax for categories
        categories: {
          connectOrCreate: songData.categories.map((categoryName) => ({
            where: { name: categoryName },
            create: { name: categoryName },
          })),
        },
        audioDuration: songData.audioParameters.audioDuration,
        seed: songData.audioParameters.seed,
        guidanceScale: songData.audioParameters.guidanceScale,
        inferStep: songData.audioParameters.inferStep,
        instrumental: songData.audioParameters.instrumental,
        userId: songData.userId, // Use userId from songData
      },
      include: {
        categories: true, // Include categories in the result
      },
    });
    return this.mapToSong(result);
  }

  async findById(id: string): Promise<Song | null> {
    const result = await this.prisma.song.findUnique({
      where: { id },
      include: {
        categories: true, // Include categories in the result
      },
    });
    return result ? this.mapToSong(result) : null;
  }

  async updateStatus(id: string, status: SongStatus): Promise<Song> {
    const result = await this.prisma.song.update({
      where: { id },
      data: { status },
      include: {
        categories: true,
      },
    });
    return this.mapToSong(result);
  }

  async updateWithAudioData(
    id: string,
    audioR2Key: string,
    coverImageR2Key: string,
    categories: string[],
  ): Promise<Song> {
    const result = await this.prisma.song.update({
      where: { id },
      data: {
        status: SongStatus.COMPLETED,
        audioR2Key,
        coverImageR2Key,
        // Fix: Use proper Prisma relation syntax for updating categories
        categories: {
          set: [], // First disconnect all existing categories
          connectOrCreate: categories.map((categoryName) => ({
            where: { name: categoryName },
            create: { name: categoryName },
          })),
        },
      },
      include: {
        categories: true,
      },
    });
    return this.mapToSong(result);
  }

  private mapToSong(dbSong: any): Song {
    return {
      id: dbSong.id,
      userId: dbSong.userId, // Include userId in the mapping
      status: dbSong.status as SongStatus,
      generationType: dbSong.generationType,
      prompt: dbSong.prompt,
      lyrics: dbSong.lyrics,
      describedLyrics: dbSong.describedLyrics,
      fullDescribedSong: dbSong.fullDescribedSong,
      audioR2Key: dbSong.audioR2Key,
      coverImageR2Key: dbSong.coverImageR2Key,
      // Fix: Map the categories relation to string array
      categories: dbSong.categories?.map((cat: any) => cat.name) || [],
      audioParameters: {
        audioDuration: dbSong.audioDuration,
        seed: dbSong.seed,
        guidanceScale: dbSong.guidanceScale,
        inferStep: dbSong.inferStep,
        instrumental: dbSong.instrumental,
      },
      createdAt: dbSong.createdAt,
      updatedAt: dbSong.updatedAt,
    };
  }
}
