import os
from pathlib import Path
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict
import win32com.client


class ProgramSearcherAI:
    def __init__(self, model_name='paraphrase-multilingual-MiniLM-L12-v2'):

        self.model = SentenceTransformer(model_name)
        self.programs = {}
        self.desktop_paths = [
            os.path.join(os.environ['USERPROFILE'], 'Desktop'),
            os.path.join(os.environ['PUBLIC'], 'Desktop')
        ]
        self._load_all_shortcuts()

    def _load_all_shortcuts(self):
        self.shortcuts = []
        self.shortcut_names = []
        self.shortcut_embeddings = []

        for desktop_path in self.desktop_paths:
            if os.path.exists(desktop_path):
                for lnk_file in Path(desktop_path).glob('*.lnk'):
                    program_name = self._get_shortcut_info(str(lnk_file))

                    self.shortcuts.append({
                        'path': str(lnk_file),
                        'filename': lnk_file.stem,
                        'program_name': program_name
                    })
                    self.shortcut_names.append(f"{lnk_file.stem} {program_name}")

        if self.shortcut_names:
            self.shortcut_embeddings = self.model.encode(
                self.shortcut_names,
                convert_to_numpy=True
            )

    def _get_shortcut_info(self, lnk_path: str) -> str:
        try:
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(lnk_path)
            target = shortcut.TargetPath
            if target:
                return os.path.basename(target).lower()
        except:
            pass
        return ""

    def search_semantic(self, query: str, threshold: float = 0.3, top_k: int = 5) -> List[Dict]:

        if not self.shortcuts:
            return []

        query_embedding = self.model.encode([query], convert_to_numpy=True)[0]

        similarities = np.dot(self.shortcut_embeddings, query_embedding) / (
                np.linalg.norm(self.shortcut_embeddings, axis=1) *
                np.linalg.norm(query_embedding)
        )

        top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []
        for idx in top_indices:
            if similarities[idx] > threshold:
                results.append({
                    **self.shortcuts[idx],
                    'similarity': float(similarities[idx]),
                    'type': 'semantic'
                })

        return results

    def search_keyword(self, program_name: str) -> List[Dict]:
        program_name_lower = program_name.lower()
        results = []

        for shortcut in self.shortcuts:
            if (program_name_lower in shortcut['filename'].lower() or
                    program_name_lower in shortcut['program_name'].lower()):
                results.append({
                    **shortcut,
                    'similarity': 1.0,
                    'type': 'keyword'
                })

        return results

    def hybrid_search(self, query: str, weight_semantic: float = 0.7,
                      weight_keyword: float = 0.3) -> List[Dict]:

        semantic_results = self.search_semantic(query, threshold=0.1)
        keyword_results = self.search_keyword(query)

        all_results = {}

        for result in semantic_results:
            key = result['path']
            if key not in all_results:
                all_results[key] = result
                all_results[key]['final_score'] = result['similarity'] * weight_semantic

        for result in keyword_results:
            key = result['path']
            if key in all_results:
                all_results[key]['final_score'] += 1.0 * weight_keyword
                all_results[key]['type'] = 'hybrid'
            else:
                all_results[key] = result
                all_results[key]['final_score'] = 1.0 * weight_keyword

        sorted_results = sorted(
            all_results.values(),
            key=lambda x: x['final_score'],
            reverse=True
        )

        return sorted_results

    def launch_program(self, lnk_path: str) -> bool:
        try:
            os.startfile(lnk_path)
            return True
        except Exception as e:
            print(f"Ошибка запуска {lnk_path}: {e}")
            return False

    def search_and_launch(self, query: str, launch_best: bool = True) -> Dict:

        results = self.hybrid_search(query)

        if not results:
            print(f"Ярлыки, похожие на '{query}', не найдены.")
            return {"found": False, "results": []}

        print(f"\nНайдено {len(results)} похожих ярлыков:")
        for i, result in enumerate(results[:5], 1):
            print(f"{i}. {result['filename']} "
                  f"(схожесть: {result['final_score']:.2%})")
            if result['program_name']:
                print(f"   Программа: {result['program_name']}")

        if launch_best and results:
            best_result = results[0]
            print(f"\nЗапускаю: {best_result['filename']}")
            self.launch_program(best_result['path'])

        return {"found": True, "results": results, "launched": launch_best}


searcher = ProgramSearcherAI()

queries = [
        "телеграм"
    ]

for query in queries:
    print(f"Поиск: '{query}'")
    searcher.search_and_launch(query, launch_best=False)


#searcher.search_and_launch("planetvpn", launch_best=True)