import { NextRequest, NextResponse } from 'next/server';
import { readFile } from 'fs/promises';
import { join } from 'path';

export async function GET(
  request: NextRequest,
  { params }: { params: { featureId: string } }
) {
  try {
    const { featureId } = params;

    // Map feature IDs to migration guide files
    const migrationGuideMap: Record<string, string> = {
      'acs-email-service': 'email-service-migration.md',
      // Add more mappings as needed
    };

    const fileName = migrationGuideMap[featureId];

    if (!fileName) {
      return NextResponse.json(
        { error: 'Migration guide not found for this feature' },
        { status: 404 }
      );
    }

    const filePath = join(process.cwd(), 'migration-guides', fileName);
    const content = await readFile(filePath, 'utf-8');

    return new NextResponse(content, {
      headers: {
        'Content-Type': 'text/markdown',
      },
    });
  } catch (error) {
    console.error('Error reading migration guide:', error);
    return NextResponse.json(
      { error: 'Failed to load migration guide' },
      { status: 500 }
    );
  }
}
