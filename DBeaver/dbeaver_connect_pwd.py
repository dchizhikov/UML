import json

def rename_db_by_etalon(data):
    '''
    # Получаем имена баз из _Архив/
    db_names = []
    for conn in data.get('connections', {}).values():
        folder = conn.get('folder', '')
        if folder.startswith('_Архив/'):
            db_name = conn.get('configuration', {}).get('database')
            if db_name:
                db_names.append(db_name)
    '''
    # Ручное определение db_names для примера (в реальном коде закомментируйте эту строку)
    db_names = ['cnt_prod_ro', 'cnt_dev_ro', 'cnt_stage_ro', 'contingent', 'gateway', 'gateway', 'cnt_stage_ro_lk', 'ezd_stage_ro_2021', 'nsi3_stage_ro', 'nsi3api_stage_ro', 'ezd_stage_ro', 'ezd_stage_ro_logs', 'ezd_stage_ro_int_lms', 'ezd_stage_ro_int_cnt', 'ezd_stage_ro_soc', 'ezd_stage_ro_ae', 'ezd_stage_ro_sbc', 'ezd_stage_ro_acl', 'ezd_stage_ro_marks', 'ezd_stage_ro_epgu', 'eom_stage_ro', 'eom_stage_ro_mresh', 'eom_stage_ro_acl', 'eom_stage_ro_acl_mresh', 'lrs_stage_ro', 'postgres', 'nsi', 'aupd_prod_ro', 'aupd_prod_ro_esia', 'aupd_prod_ro_sudir', 'aupd_prod_ro_kauth', 'aupd_stage_ro', 'aupd_stage_ro_esia', 'aupd_stage_ro_sudir', 'aupd_stage_ro_kauth', 'aupd_stage_ro_dim', 'vibor_stage_ro_material']

    # Находим соединения в "МЭШ"
    mesh_conns = []
    for conn_id, conn in data.get('connections', {}).items():
        if conn.get('folder', '') == 'МЭШ':
            mesh_conns.append((conn_id, conn))

    # Проверяем, что количество совпадает
    if len(mesh_conns) != len(db_names):
        print(len(mesh_conns), len(db_names))
        raise ValueError("Количество соединений в 'МЭШ' не совпадает с количеством баз из _Архив/")

    # Переименовываем name, database и URL
    for (conn_id, conn), new_name in zip(mesh_conns, db_names):
        conn['name'] = new_name
        if 'configuration' in conn:
            conn['configuration']['database'] = new_name
            if 'url' in conn['configuration']:
                old_url = conn['configuration']['url']
                pos = old_url.rfind('/')
                new_url = old_url[:pos+1] + new_name
                conn['configuration']['url'] = new_url

def replace_mesh_keys_with_etalon(data):
    connections = data.get('connections', {})

    # Получаем списки ключей из папок
    mesh_items = [(k, v) for k, v in connections.items() if v.get('folder') == 'МЭШ']
    etalon_keys = [k for k, v in connections.items() if v.get('folder') == 'МЭШ.Тест']

    # Кол-во для итерации - минимальное из двух, чтобы не выйти за пределы
    count = min(len(mesh_items), len(etalon_keys))

    for i in range(count):
        mesh_key, mesh_conn = mesh_items[i]
        etalon_key = etalon_keys[i]

        # Создаём новый элемент с ключом из эталонного элемента и копируем данные из МЭШ
        connections[etalon_key] = mesh_conn.copy()
        connections[etalon_key]['folder'] = 'МЭШ'

        # Удаляем старый элемент из МЭШ
        del connections[mesh_key]


#Загрузка данных
with open('data-sources.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

rename_db_by_etalon(data)
#replace_mesh_keys_with_etalon(data)

#Сохраняем результат
with open('data-sources-renamed.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print('Переименование завершено успешно.')

#Дополнительная проверка URL
print("\nПроверка URL:")
for conn_id, conn in mesh_conns:
    conf = conn.get('configuration', {})
    if 'database' in conf and 'url' in conf:
        expected_db = conf['database']
        actual_db = conf['url'].split('/')[-1]
        status = "OK" if expected_db == actual_db else "ERROR"
        print(f"[{status}] {conn_id}: {expected_db} == {actual_db}")