import { inngest } from "../../inngest/client";
import type { QueueService } from "../../core/ports/interfaces";

export class InngestQueueService implements QueueService {
  async queueSong(songId: string, data: any): Promise<void> {
    await inngest.send({
      name: "song/generate",
      data: {
        songId,
        ...data,
      },
    });
  }
}
