import { readFileSync, readdirSync, statSync, unlinkSync, writeFileSync } from "fs";
import GPT3Tokenizer from "gpt3-tokenizer";
import { join } from "path";

const tokenizer = new GPT3Tokenizer({ type: "gpt3" });
const tokenLimit = 1000;

const getDirectoryFilesRecursively = (directoryPath: string, filepaths: string[]) => {
  readdirSync(directoryPath).forEach((file) => {
    const Absolute = join(directoryPath, file);
    if (statSync(Absolute).isDirectory()) return getDirectoryFilesRecursively(Absolute, filepaths);
    else return filepaths.push(Absolute);
  });
  return filepaths;
};

const getFileStartPrefix = (
  filepath: string,
  tokens: number,
  characters: number,
  firstCharacterIndex: number,
  lastCharacterIndex: number,
) =>
  `-{storyteller}:{file-start}:{filepath=${filepath}}:{tokens=${tokens}}:{characters:${characters}}:{firstCharacterIndex:${firstCharacterIndex}}:{lastCharacterIndex:${lastCharacterIndex}}-`;
const getFileEndPostfix = (filepath: string, tokens: number, characters: number) =>
  `-{storyteller}:{file-start}:{filepath=${filepath}}:{tokens=${tokens}}:{characters:${characters}}-`;

type Chunk = { start: number; end: number; content: string };

const splitToChunks = (str: string, limit: number): Chunk[] => {
  var chunks: Chunk[] = [];
  for (let start = 0; start < str.length; start += limit) {
    const content = str.substring(start, start + limit);
    chunks.push({ content, start, end: start + content.length });
  }
  return chunks;
};

const formatFilesForTokenizerLimit = (filepaths: string[]): { filepath: string; chunks: string[] }[] =>
  filepaths.map((filepath) => {
    const file = readFileSync(filepath).toString();
    const allTokens = tokenizer.encode(file).text.length;
    if (allTokens < tokenLimit) {
      const modifiedFile = `${getFileStartPrefix(
        filepath,
        allTokens,
        file.length,
        0,
        allTokens,
      )}\n${file}\n${getFileEndPostfix(filepath, allTokens, file.length)}`;
      // const newTokens = tokenizer.encode(modifiedFile).text.length;
      // if (newTokens > tokenLimit) {
      //   throw Error("new Tokens must be less than token limit");
      // }
      return { filepath, chunks: [modifiedFile] };
    } else {
      const chunks = splitToChunks(file, tokenLimit);
      const chunksWithTokens = chunks.map((chunk) => ({
        ...chunk,
        tokens: tokenizer.encode(chunk.content).text.length,
      }));
      const modifiedChunks = chunksWithTokens.map(
        (chunk) =>
          `${getFileStartPrefix(filepath, allTokens, file.length, chunk.start, chunk.end)}\n${
            chunk.content
          }\n${getFileEndPostfix(filepath, allTokens, file.length)}`,
      );
      return { filepath, chunks: modifiedChunks };
    }
  });

const chunkDirFiles = (directoryPath: string) => {
  const directoryFilepaths = getDirectoryFilesRecursively(directoryPath, []).filter(
    (filepath) =>
      filepath.includes(".spec.ts") === false &&
      filepath.includes("/node_modules/") === false &&
      filepath.includes("/docs/") === false &&
      filepath.includes("/.git/") === false &&
      filepath.includes("/package-lock.json") === false,
  );
  const files = formatFilesForTokenizerLimit(directoryFilepaths);
  files.forEach((file) => {
    const newFilePath = `./files/${file.filepath.replace(/\//g, "-")}`;

    file.chunks.forEach((chunk, index) => {
      writeFileSync(newFilePath + `-${index}`, chunk);
    });
  });
};
readdirSync("./files").forEach((filename) => {
  unlinkSync(`./files/${filename}`);
});
chunkDirFiles("/home/lukasz/workspace/storyteller/packages/storyteller/src");
chunkDirFiles("/home/lukasz/workspace/storyteller/repositories/examples/5.1-real-life-scenario");

readdirSync("./files").forEach((filename) => {
  const content = readFileSync(`./files/${filename}`).toString();
  if (tokenizer.encode(content).text.length > 1024) {
    console.log("FAILED", filename);
  }
});
