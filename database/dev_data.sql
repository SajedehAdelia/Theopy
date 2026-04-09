BEGIN;

INSERT INTO company (company_id, name, address, city, postal_code, phone, fax, email, company_type, rcs, siren, tva_registration, naf, website, capital, logo) VALUES
(100, 'Prestataire', '1 rue de la Paix', 'Villeurbanne', '69100', '01 23 45 67 89', '09 87 65 43 21', 'prestataire@me.fr', 'Pharmacie', '123 456 789', '362 521 879 00034', 'FR 01 123456789', '6969Z', 'prestataire.fr', NULL, NULL),
(101, 'Pharmacie de la Gare', '1 rue de la Gare', 'Oullins', '69600', '01 23 45 67 89', '09 87 65 43 21', 'pharmadelagare@me.fr', 'Pharmacie', '123 456 789', '', '', '', 'pharmadelagare.fr', NULL, NULL),
(102, 'Pharmacie du Soleil', '1 boulevard du Soleil', 'Saint Denis', '97400', '01 23 45 67 89', '09 87 65 43 21', 'pharmadusoleil@me.fr', 'Pharmacie', '123 456 789', '', '', '', 'pharmadusoleil.fr', NULL, NULL),
(103, 'Pharmacie de la Nuit', '1 avenue du Moulin Rouge', 'Paris', '75000', '01 23 45 67 89', '09 87 65 43 21', 'pharmadelanuit@me.fr', 'Pharmacie', '123 456 789', '', '', '', 'pharmadelanuit.fr', NULL, NULL),
(104, 'Grande Pharmacie des Gones', '1 place de la Garde', 'Lyon', '69000', '01 23 45 67 89', '09 87 65 43 21', 'pharmadesgones@me.fr', 'Pharmacie', '123 456 789', '', '', '', 'pharmadesgones.fr', NULL, NULL),
(105, 'Méchant Groupement', '1 rue des enfers', 'Lyon', '69000', '01 23 45 67 89', '09 87 65 43 21', 'evilgroup@me.fr', 'Groupement', '123 456 789', '', '', '', 'evilgroup.fr', NULL, NULL),
(106, 'CPAM Rhône', '1 rue de la Part-Dieu', 'Lyon', '69000', '01 23 45 67 89', '09 87 65 43 21', 'contact@cpam-rhone.fr', 'Pharmacie', '123 456 789', '', '', '', 'cpam.fr', NULL, NULL),
(107, 'Harmonie', '1 place Bellecour', 'Lyon', '69000', '01 23 45 67 89', '09 87 65 43 21', 'contact@harmonie.fr', 'Pharmacie', '123 456 789', '', '', '', 'harmonie.fr', NULL, NULL),
(108, 'Méchante Pharmacie', '1 rue des enfers', 'Lyon', '69000', '01 23 45 67 89', '09 87 65 43 21', 'evilpharma@me.fr', 'Groupement', '123 456 789', '362 521 879 00034', '', '', 'evilpharma.fr', NULL, NULL),
(109, 'Pharmacie du Hamac', '1 rue du Hamac', 'Guyane Française', '97320', '01 23 45 67 89', '09 87 65 43 21', 'pharmaduhamac@me.fr', 'Pharmacie', '123 456 789', '', '', '', 'pharmaduhamac.fr', NULL, 'https://i.picsum.photos/id/237/536/354.jpg?hmac=i0yVXW1ORpyCZpQ-CknuyV-jbtU7_x9EBQVhvT5aRr0'),
(110, 'Pharmacie 6 Laphamille', '1 rue des Remèdes', 'Lyon', '69000', '01 23 45 67 89', '09 87 65 43 21',  'pharma6@me.fr', 'Pharmacie', '123 456 789', '', '', '', 'pharmacie6.fr', NULL, NULL);

-- Passwords are "test"
INSERT INTO "user" (user_id, login, password, name, email, phone, calendar_color, code, company_id, role_type, active, last_activity) VALUES
(100, 'slamotte', '\x2470626b6466322d73686135313224323530303024476150554f716430546f6d524d755a6369354579686724304d7067316e36315a576470704353316b487a65494b58734437644b786643796a576a5a4a62317269526a4d3654626f7575484c614938645645426d6d6e4c6935566766753948684c32754c724b694264612f736651', 'Sylvie Lamotte', 'sylvie@example.com', NULL, NULL, 'SL', 100, 'administrator', true, '2023-10-01 12:00:00'),
(101, 'monesime', '\x2470626b6466322d73686135313224323530303024476150554f716430546f6d524d755a6369354579686724304d7067316e36315a576470704353316b487a65494b58734437644b786643796a576a5a4a62317269526a4d3654626f7575484c614938645645426d6d6e4c6935566766753948684c32754c724b694264612f736651', 'Mathieu Onésime', 'mathieu@example.com', '01 23 45 67 89', '#729fcf', NULL, 100, 'manager', true, '2023-09-15 08:30:00'),
(102, 'cbeauchamp', '\x2470626b6466322d73686135313224323530303024476150554f716430546f6d524d755a6369354579686724304d7067316e36315a576470704353316b487a65494b58734437644b786643796a576a5a4a62317269526a4d3654626f7575484c614938645645426d6d6e4c6935566766753948684c32754c724b694264612f736651', 'Christelle Beauchamp', 'christelle@example.com', '01 23 67 45 89', '#729fcf', NULL, 100, 'manager', true, '2023-09-20 14:45:00'),
(103, 'fbelzebuth', '\x2470626b6466322d73686135313224323530303024476150554f716430546f6d524d755a6369354579686724304d7067316e36315a576470704353316b487a65494b58734437644b786643796a576a5a4a62317269526a4d3654626f7575484c614938645645426d6d6e4c6935566766753948684c32754c724b694264612f736651', 'Fabienne Belzebuth', 'fabienne@example.com', '01 23 67 45 89', '#729fcf', NULL, 106, 'manager', true, '2023-08-10 10:15:00'),
(104, 'jclement', '\x2470626b6466322d736861353132243235303030244b7357596b354c79767663656f35537974686169744124476d393132454962346b4e686d5643494a69302f6766733063547235473441672e5048664f513078532e46454970704b715632437a31456470344a45534571474d434b356677333656574c4b77383730455071374377', 'Jessica Clément', 'jessica@example.com', '', '#f57900', NULL, 100, 'operator', true, '2023-07-25 16:00:00'),
(105, 'sblameau', '\x2470626b6466322d736861353132243235303030244b7357596b354c79767663656f35537974686169744124476d393132454962346b4e686d5643494a69302f6766733063547235473441672e5048664f513078532e46454970704b715632437a31456470344a45534571474d434b356677333656574c4b77383730455071374377', 'Stéphane Blameau', 'stephane@example.com', '', '#f57900', NULL, 100, 'operator', true, '2023-06-30 09:00:00'),
(106, 'jtessier', '\x2470626b6466322d736861353132243235303030244b7357596b354c79767663656f35537974686169744124476d393132454962346b4e686d5643494a69302f6766733063547235473441672e5048664f513078532e46454970704b715632437a31456470344a45534571474d434b356677333656574c4b77383730455071374377', 'Jeanette Tessier', 'jeanette@example.com', '', '#f57900', NULL, 100, 'operator', true, '2023-05-15 11:30:00'),
(107, 'abeaulne', '\x2470626b6466322d73686135313224323530303024476150554f716430546f6d524d755a6369354579686724304d7067316e36315a576470704353316b487a65494b58734437644b786643796a576a5a4a62317269526a4d3654626f7575484c614938645645426d6d6e4c6935566766753948684c32754c724b694264612f736651', 'Amandine Beaulne', 'amandine@example.com', NULL, NULL, 'SL', 100, 'commercial', true, '2023-04-01 13:00:00'),
(108, 'vcosette', '\x2470626b6466322d73686135313224323530303024476150554f716430546f6d524d755a6369354579686724304d7067316e36315a576470704353316b487a65494b58734437644b786643796a576a5a4a62317269526a4d3654626f7575484c614938645645426d6d6e4c6935566766753948684c32754c724b694264612f736651', 'Victoire Cosette', 'victoire@example.com', NULL, NULL, 'SL', 100, 'commercial', true, '2023-03-10 17:45:00'),
(109, 'fgivry', '\x2470626b6466322d73686135313224323530303024476150554f716430546f6d524d755a6369354579686724304d7067316e36315a576470704353316b487a65494b58734437644b786643796a576a5a4a62317269526a4d3654626f7575484c614938645645426d6d6e4c6935566766753948684c32754c724b694264612f736651', 'Frédérique Givry', 'frederique@example.com', NULL, NULL, 'FG', 100, 'commercial', true, '2023-02-20 14:00:00'),
(110, 'cdubois', '\x2470626b6466322d736861353132243235303030246b68496935447748414f4238372f316671335875335124496e47693772786633464a7477586c634e66763434597575574262506d702f446452437258563049347a6936534b626e7845647665772e5147327a62487371463852616876414b724167452e46546f74666849703167', 'Charles Dubois', 'charles@example.com', NULL, NULL, 'CDB', 101, 'employee', false, '2023-01-05 10:30:00'),
(111, 'jcdenis', '\x2470626b6466322d736861353132243235303030244b7357596b354c79767663656f35537974686169744124476d393132454962346b4e686d5643494a69302f6766733063547235473441672e5048664f513078532e46454970704b715632437a31456470344a45534571474d434b356677333656574c4b77383730455071374377', 'Jean-Charles Denis', 'jcdenis@example.com', NULL, NULL, '123', 102, 'employee', true, '2022-12-15 08:00:00'),
(112, 'pdelavergne', '\x2470626b6466322d736861353132243235303030244b7357596b354c79767663656f35537974686169744124476d393132454962346b4e686d5643494a69302f6766733063547235473441672e5048664f513078532e46454970704b715632437a31456470344a45534571474d434b356677333656574c4b77383730455071374377', 'Pénélope de la Vergne', 'penelope@example.com', NULL, NULL, '666', 103, 'employee', true, '2022-11-10 15:15:00'),
(113, 'cmartel', '\x2470626b6466322d736861353132243235303030244b7357596b354c79767663656f35537974686169744124476d393132454962346b4e686d5643494a69302f6766733063547235473441672e5048664f513078532e46454970704b715632437a31456470344a45534571474d434b356677333656574c4b77383730455071374377', 'Carine Martel', 'carine@example.com', NULL, NULL, '666', 104, 'employee', true, '2022-10-05 09:45:00'),
(114, 'blepicier', '\x2470626b6466322d736861353132243235303030244b7357596b354c79767663656f35537974686169744124476d393132454962346b4e686d5643494a69302f6766733063547235473441672e5048664f513078532e46454970704b715632437a31456470344a45534571474d434b356677333656574c4b77383730455071374377', 'Bertrand Lépicier', 'bertrand@example.com', NULL, NULL, '666', 108, 'employee', true, '2022-09-01 13:30:00'),
(115, 'kbettencourt', '\x2470626b6466322d736861353132243235303030246b68496935447748414f4238372f316671335875335124496e47693772786633464a7477586c634e66763434597575574262506d702f446452437258563049347a6936534b626e7845647665772e5147327a62487371463852616876414b724167452e46546f74666849703167', 'Karine Bettencourt', 'karine@example.com', '01 23 45 67 89', '#729fcf', NULL, 100, 'manager', false, '2022-08-20 11:00:00'),
(116, 'mgarcia', '\x2470626b6466322d736861353132243235303030244b7357596b354c79767663656f35537974686169744124476d393132454962346b4e686d5643494a69302f6766733063547235473441672e5048664f513078532e46454970704b715632437a31456470344a45534571474d434b356677333656574c4b77383730455071374377', 'Maurice Garcia', 'maurice@example.com', NULL, NULL, '394', 109, 'employee', true, '2022-07-15 14:30:00'),
(200, 'cprala', '\x2470626b6466322d736861353132243235303030244b7357596b354c79767663656f35537974686169744124476d393132454962346b4e686d5643494a69302f6766733063547235473441672e5048664f513078532e46454970704b715632437a31456470344a45534571474d434b356677333656574c4b77383730455071374377', 'Charlotte Prala', 'charlotte@example.com', NULL, NULL, 'CPA', 108, 'operator', true, '2022-06-10 10:00:00'),
(201, 'mevictorlieu', '\x2470626b6466322d736861353132243235303030244b7357596b354c79767663656f35537974686169744124476d393132454962346b4e686d5643494a69302f6766733063547235473441672e5048664f513078532e46454970704b715632437a31456470344a45534571474d434b356677333656574c4b77383730455071374377', 'Marie-Élisabeth Victorlieu', 'mevictorlieu@example.com', NULL, NULL, 'CPA', 100, 'contractor', true, '2022-05-05 12:15:00'),
(202, 'pouet', '\x2470626b6466322d736861353132243235303030244b7357596b354c79767663656f35537974686169744124476d393132454962346b4e686d5643494a69302f6766733063547235473441672e5048664f513078532e46454970704b715632437a31456470344a45534571474d434b356677333656574c4b77383730455071374377', 'Pierre Ouet', 'pouet@example.com', NULL, NULL, 'CPA', 110, 'employee', true, '2022-04-01 16:45:00'),
-- Inactive user with empty password
(220, 'rvesvrotte', '\x2470626b6466322d73686135313224323530303024433647304e6d5a4d7158554f6758427554656b397077247263386e54336a72576f70473544507631793250575a5a756963746730524a43653378396c4e4a76692e414e72396c6e67653976707a4d5468466646463856507a714174686346573167684672524f545439414a4151', 'Charles Richard de Vesvrotte', 'rvesvrotte@example.com', NULL, NULL, 'CRV', 100, 'commercial', false, '2022-03-01 09:00:00');

INSERT INTO "user_preferences" (user_id, sidebar_collapsed) VALUES
(100, true),
(101, false),
(102, true),
--user_id 103 has no preferences for testing purpose
(104, true),
(105, false),
(106, true),
(107, false),
(108, true),
(109, false),
(110, true),
(111, false),
(112, true),
(113, false),
(114, true),
(115, false),
(116, true),
(200, true),
(201, false),
(202, true);

INSERT INTO healthcare_software (healthcare_software_id, name, active) VALUES
(100, 'LGPI', true),
(101, 'Ospharm', true),
(102, 'Xana', true),
(103, 'GLaDOS', true);

INSERT INTO customer (customer_id, healthcare_company_type, company_id, balance_target, rejection_rate_target, concentrator_login, concentrator_password, holder_name, finess, activity_start, cps_card_code, operator_code_to_use, remote_print, rejection_channel, rejection_channel_login, rejection_channel_password, opening_hours, documents_channel, patient_contact, to_credit_instructions, had_at_management, prescription_rights_restriction, concentrator_name, general_info, bic, iban, frequency, referent_id, bank_name, to_debit, hide_logo, billing_address, origin, commercial_follow_up_id, hidden_fse, invoicing_email, healthcare_software_id) VALUES
(100, 'pharmacy', 101, NULL, NULL, '', '', 'Marcel Dumont', '382918343', NULL, '', '', false, '', '', '', 'Ouvert tous les jours de 9h à 19h', '', false, '', false, '', '', '', 'SOGEFRPP', 'FR7630003014700002027581897', '', NULL, 'Société Générale', true, false, E'1 rue de la gare\r\n69600 Oullins', '', 107, '{}', 'invoices@example.com', 100),
(101, 'pharmacy', 102, NULL, NULL, '', '', 'Jean-Charles Denis', '748392775', NULL, '', '', false, '', '', '', 'Ouvert tous les jours de 9h à 19h', '', false, '', false, '', '', '', 'CRLYFRPPXXX', 'FR9217569000709992564438E20', '', NULL, 'LCL', true, false, E'1 rue boulevard Soleil\r\n97400 Saint Denis', '', NULL, '{}', NULL, 101),
(102, 'pharmacy', 103, NULL, NULL, '', '', 'Pénélope De La Vergne', '193759205', NULL, '', '', false, '', '', '', 'Ouvert tous les jours de 9h à 23h', '', false, '', false, '', '', '', 'BNPAFRPHXXX', 'FR7517569000409696632224H74', '', NULL, 'BNP Paribas', true, false, E'1 avenue du Moulin Rouge\r\n75000 Paris', '', 108, '{}', NULL, 102),
(103, 'pharmacy', 104, NULL, NULL, '', '', 'Carine Martel', '395750749', NULL, '', '', false, '', '', '', 'Ouvert tous les jours de 9h à 19h', '', false, '', false, '', '', '', 'CMCIFRPAXXX', 'FR0414508000301716793327B47', '', NULL, 'Crédit Mutuel', true, false, E'1 place de la Garde\r\n69000 Lyon', '', 109, '{}', NULL, 103),
(104, 'pharmacy', 109, NULL, NULL, '', '', 'Pierre Martin', '193473759', NULL, '', '', false, '', '', '', 'Ouvert tous les jours de 9h à 19h', '', false, '', false, '', '', '', 'AGRIMQMX', 'FR9210096000509594643953I08', '', NULL, 'Crédit Agricole', true, true, E'1 place du Hamac \r\n97320 Guyane Française', '', 107, '{}', NULL, 102 ),
(200, 'pharmacy', 108, NULL, NULL, '', '', 'Bertrand Lépicier', '975029577', NULL, '', '', false, '', '', '', 'Ouvert tous les jours de 9h à 19h', '', false, '', false, '', '', '', 'CMCIFRPAXXX', 'FR0414508000301716793327B47', '', NULL, 'Crédit Mutuel', true, false, E'1 place des enfers \r\n69000 Lyon', '', NULL, '{}', NULL, 101),
(201, 'pharmacy', 110, NULL, NULL, '', '', 'Jean Peuplus', '975029577', NULL, '', '', false, '', '', '', 'Ouvert tous les jours de 9h à 19h', '', false, '', false, '', '', '', 'CMCIFRPAXXX', 'FR0414508000301716793327B47', '', NULL, 'Crédit Mutuel', true, false, E'1 rue des Remèdes \r\n69000 Lyon', '', NULL, '{}', NULL, 100);

INSERT INTO managed_customer (managed_customer_id, manager_id, customer_id) VALUES
(100, 101, 100),
(101, 101, 101),
(102, 102, 102),
(103, 102, 103),
(104, 103, 103),
(105, 101, 104),
(106, 201, 101),
(200, 200, 200);

INSERT INTO provider (provider_id, company_id) VALUES
(100, 100),
(101, 104),
(102, 106),
(103, 107),
(104, 101),
(200, 108),
(201, 110);

INSERT INTO contract (contract_id, provider_id, customer_id, has_subscription, has_mailing_fees, price, start, "end") VALUES
(100, 100, 100, true, false, 29.90, '2019-01-01', '2020-12-31'),
(101, 100, 100, true, true, 29.90, '2021-01-01', '2040-12-31'),
(102, 100, 101, true, true, 9.90, '2019-01-01', NULL),
(103, 100, 102, true, false, 29.90, '2019-01-01', now()), -- Current time cannot be mocked in postgresql
(104, 100, 103, true, false, 9.90, '2019-01-01', '2019-05-31'),
(105, 100, 103, true, true, 9.90, '2019-06-01', '2020-12-31'),
(106, 100, 104, true, true, 9.90, '2019-06-01', NULL),
(200, 200, 200, true, false, 0, '2019-01-01', NULL),
(201, 201, 201, true, false, 69.42, '2019-01-01', NULL);

INSERT INTO service (service_id, code, name, monthly_plan, provider_id) VALUES
(100, 'BOSH', 'Gestion du tiers payant à l''heure', false, 100),
(101, 'BOSP', 'Promotion sur la gestion du tiers-payant', false, 100),
(102, 'BOG', 'Gestion interne du tiers payant', false, 100),
(103, 'BOSF', 'Délégation Forfait', true, 100);

INSERT INTO contract_line (contract_line_id, contract_id, service_id, price_no_tax, hour_quota) VALUES
(100, 100, 100, 40, NULL),
(101, 101, 100, 40, NULL),
(102, 102, 101, 40, NULL),
(103, 103, 100, 40, NULL),
(104, 104, 100, 40, NULL),
(105, 105, 100, 40, NULL),
(106, 106, 103, 40, 8),
(200, 200, 102, 40, NULL),
(201, 201, 102, 40, NULL);

INSERT INTO customer_bank (customer_bank_id, customer_id, iban, bic, start, "end", account_holder) VALUES
(100, 100, 'FR7630003014700002027581897', 'SOGEFRPP', '2018-01-01 00:00:00', '2019-12-31 00:00:00', 'Marcel Dumont'),
(101, 100, 'FR5130003000302751312838L44', 'SOGEFRPP', '2020-01-01 00:00:00', '2021-12-31 00:00:00', 'Marcel Dumont'),
(102, 101, 'FR9217569000709992564438E20', 'CRLYFRPPXXX', '2019-01-01 00:00:00', '2021-12-31 00:00:00', 'Jean-Charles Denis'),
(103, 102, 'FR7517569000409696632224H74', 'BNPAFRPHXXX', '2019-01-01 00:00:00', '2022-12-31 00:00:00', 'Pénélope De La Vergne'),
(104, 103, 'FR0414508000301716793327B47', 'CMCIFRPAXXX', '2019-01-01 00:00:00', NULL, 'Carine Martel'),
(105, 104, 'FR9210096000509594643953I08', 'AGRIMQMX', '2019-01-01 00:00:00', NULL, 'Pierre Martin'),
(200, 200, 'FR5710096000306755197562G41', 'AGRIMQMX', '2019-01-01 00:00:00', NULL, 'Bertrand Lépicier'),
(201, 201, 'FR5710096000306755197562G41', 'AGRIMQMX', '2019-01-01 00:00:00', NULL, NULL);

INSERT INTO customer_provider (customer_id, provider_id) VALUES
(100, 100),
(101, 100),
(102, 100),
(103, 100),
(104, 100),
(200, 200),
(201, 201);

INSERT INTO customer_stat (customer_stat_id, customer_id, balance_one_month, balance_one_year, balance_two_year, emitted_invoices, nb_of_rejects, rejects_amount, insertion_date) VALUES
(100, 100, 21.0, 450.0, 1200.0, 43, 21, 33.45, '2019-05-23 17:51:45.883621'),
(101, 100, 12.12, 89.2, 190.0, 3, 2, 12.34, '2019-04-23 17:50:39.24616');

INSERT INTO customer_document (document_id, customer_id, mimetype, filename, "date", content) VALUES
(100, 100, 'text/plain', 'document.txt', '2019-04-12', 'blablabla'),
(101, 100, 'text/plain', 'document2.txt', '2019-04-12', 'bouboubou'),
(102, 102, 'text/plain', 'document.txt', '2019-04-12', 'baubaubau');

INSERT INTO intervention (intervention_id, customer_id, provider_id, operator_id, service_id, start, "end", comments, agreement_pending, charged_duration, balance_one_month, mail_count) VALUES
(100, 100, 100, 101, 100, '2019-05-21 09:32:18', '2019-05-21 12:32:17', 'C''était une intervention intéressante.', false, '04:30:00',  1792.39, 2),
(101, 100, 100, 102, 100, '2019-05-22 09:32:18', '2019-05-22 12:12:44', 'C''était une intervention très intéressante.', false, '02:30:00', 1290.45, 3),
(102, 100, 100, 101, 100, '2019-05-28 09:32:18', '2019-05-28 12:32:17', 'C''était une intervention hyper intéressante.', false, '04:30:00', 1359.22, 0),
(103, 100, 100, 101, 100, '2019-05-31 09:32:18', '2019-05-31 12:32:17', 'C''était une intervention ultra intéressante.', false, '04:30:00', 2932.42, 4),
(104, 100, 100, 101, 100, '2021-05-31 09:32:18', '2021-05-31 12:32:17', 'C''était une intervention ultra intéressante.', true, '04:30:00', 2503.10, 4),
(105, 104, 100, 101, 103, '2022-05-31 09:32:18', '2022-05-31 10:32:17', 'C''était une intervention ultra intéressante.', false, '01:00:00', 1203.59, 0),
(106, 100, 100, 101, 100, '2022-05-31 09:32:18', '2022-05-31 10:32:17', 'C''était une intervention ultra intéressante.', false, '01:00:00', 331.95, 0),
(107, 104, 100, 101, 103, '2019-04-15 09:32:18', '2019-04-15 10:32:17', 'C''était une intervention ultra intéressante.', false, '01:00:00', 1203.59, 0),
(200, 200, 200, 200, 102, '2019-05-31 09:32:18', '2019-05-31 12:32:17', 'C''était une intervention ultra intéressante.', false, '04:30:00', 2034, 0),
(108, 100, 100, 101, 100, '2025-12-22 09:32:18', '2025-12-22 12:32:17', 'Test semaine 52 de 2025', false, '03:00:00', 1000.00, 1),
(109, 100, 100, 101, 100, '2025-12-29 09:32:18', '2025-12-29 12:32:17', 'Test semaine 1 de 2026 (début)', false, '03:00:00', 1100.00, 1),
(110, 100, 100, 101, 100, '2026-01-05 09:32:18', '2026-01-05 12:32:17', 'Test semaine 2 de 2026', false, '03:00:00', 1200.00, 1);


INSERT INTO intervention_action (action_id, intervention_id, action_type) VALUES
(100, 100, 'customer_credits');

INSERT INTO intervention_line (line_id, intervention_id, fse_number, rc, ro, amount, employee_id, rejection_reason, unpaid, reject, action, tool_type, contact, customer_inquiry, mail_type, fse_number_change, credit, avoir, profit_loss, npai, comment, insertion_date, mandatory_health_insurance, complementary_health_insurance, mandatory_health_insurance_code, complementary_health_insurance_code, lot_number, invoice_transmission_date, archiving, payment_date, paid_amount) VALUES
(100, 100, '123456789', false, true, 12.37, 110, 'unknown_benefits', false, true, 'recycling', 'return_email_pa', 'mail_message', 'duplicata', 'mail_client', '', 134.56, NULL, NULL, false, 'On ne sait pas qui est le bénéficiaire.', '2019-05-23 17:34:10.672632', 'CPAM Rhône', '', NULL, NULL, '333', '2019-02-08', false, NULL, NULL),
(102, 101, '123456789', false, true, 12.37, 101, 'unknown_benefits', false, true, 'recycling', 'return_email_pa', 'mail_message', 'duplicata', 'mail_client', '', 278.69, NULL, NULL, false, 'On ne sait pas qui est le bénéficiaire.', '2019-05-23 17:34:10.672632', 'CPAM Rhône', '', NULL, NULL, '333', '2019-02-08', false, NULL, NULL),
(101, 101, '987654321', true, true, 14.98, 102, 'other', true, false, 'loss', NULL, NULL, 'validate_client_mail', NULL, '', NULL, NULL, 14.98, false, 'On abandonne cet impayé.', '2019-05-23 17:42:33.150225', 'CPAM Rhône', 'Harmonie', NULL, NULL, '293', '2019-01-02', true, NULL, NULL),
(200, 200, '987654321', true, true, 14.98, 200, 'other', true, false, 'loss', NULL, NULL, 'validate_client_mail', NULL, '', NULL, NULL, 14.98, false, 'On abandonne cet impayé.', '2019-05-23 17:42:33.150225', 'CPAM Rhône', 'Harmonie', NULL, NULL, '293', '2019-01-02', true, NULL, NULL);

INSERT INTO intervention_line_letter (letter_id, line_id, content) VALUES
(100, 100, '\x255044462d');

INSERT INTO intervention_line_attachment (attachment_id, line_id, content) VALUES
(100, 100, '\x255044462d');

INSERT INTO organism (organism_id, company_id, provider_id, transmission_code, contact) VALUES
(100, 106, 100, '1234', 'Gilles Lesieur'),
(101, 107, 100, '5678', 'François Sage');

INSERT INTO planned_intervention (planned_intervention_id, hour, day, duration, customer_id, user_id, actual_intervention_id) VALUES
(10000, '09:30:00', '2019-01-01', 150, 100, 101, NULL),
(10001, '09:30:00', '2019-01-08', 150, 100, 101, NULL),
(10002, '09:30:00', '2019-01-15', 150, 100, 101, NULL),
(10003, '09:30:00', '2019-01-22', 150, 100, 101, NULL),
(10004, '09:30:00', '2019-01-29', 150, 100, 101, NULL),
(10005, '09:30:00', '2019-02-05', 150, 100, 101, NULL),
(10006, '09:30:00', '2019-02-12', 150, 100, 101, NULL),
(10007, '09:30:00', '2019-02-19', 150, 100, 101, NULL),
(10008, '09:30:00', '2019-02-26', 150, 100, 101, NULL),
(10009, '09:30:00', '2019-03-05', 150, 100, 101, NULL),
(10010, '09:30:00', '2019-03-12', 150, 100, 101, NULL),
(10011, '09:30:00', '2019-03-19', 150, 100, 101, NULL),
(10012, '09:30:00', '2019-03-26', 150, 100, 101, NULL),
(10013, '09:30:00', '2019-04-02', 150, 100, 101, NULL),
(10014, '09:30:00', '2019-04-09', 150, 100, 101, NULL),
(10015, '09:30:00', '2019-04-16', 150, 100, 101, NULL),
(10016, '09:30:00', '2019-04-23', 150, 100, 101, NULL),
(10017, '09:30:00', '2019-04-30', 150, 100, 101, NULL),
(10018, '09:30:00', '2019-05-07', 150, 100, 101, NULL),
(10019, '09:30:00', '2019-05-14', 150, 100, 101, NULL),
(10020, '09:30:00', '2019-05-21', 150, 100, 101, NULL),
(10021, '09:30:00', '2019-05-28', 150, 100, 101, NULL),
(10022, '14:00:00', '2019-05-03', 180, 100, 101, NULL),
(10023, '14:00:00', '2019-05-10', 180, 100, 101, NULL),
(10024, '14:00:00', '2019-05-17', 180, 100, 101, NULL),
(10025, '14:00:00', '2019-05-24', 180, 100, 101, NULL),
(10026, '14:00:00', '2019-05-31', 180, 100, 101, NULL),
(10027, '14:00:00', '2019-06-01', 180, 100, 101, NULL),
(10028, '14:00:00', '2019-06-07', 180, 100, 101, NULL),
(10029, '14:00:00', '2019-06-14', 180, 100, 101, NULL),
(10030, '14:00:00', '2019-06-21', 180, 100, 101, NULL),
(10031, '14:00:00', '2019-06-28', 180, 100, 101, NULL),
(10032, '14:00:00', '2019-07-05', 180, 100, 101, NULL),
(10033, '14:00:00', '2019-07-12', 180, 100, 101, NULL),
(10034, '14:00:00', '2019-07-19', 180, 100, 101, NULL),
(10035, '14:00:00', '2019-07-26', 180, 100, 101, NULL),
(10036, '14:00:00', '2019-08-02', 180, 100, 101, NULL),
(10037, '14:00:00', '2019-08-09', 180, 100, 101, NULL),
(10038, '14:00:00', '2019-08-16', 180, 100, 101, NULL),
(10039, '14:00:00', '2019-08-23', 180, 100, 101, NULL),
(10040, '14:00:00', '2019-08-30', 180, 100, 101, NULL),
(10041, '14:00:00', '2019-09-06', 180, 100, 101, NULL),
(10042, '14:00:00', '2019-09-13', 180, 100, 101, NULL),
(10043, '14:00:00', '2019-09-20', 180, 100, 101, NULL),
(10044, '14:00:00', '2019-09-27', 180, 100, 101, NULL),
(10045, '14:00:00', '2019-10-04', 180, 100, 101, NULL),
(10046, '14:00:00', '2019-10-11', 180, 100, 101, NULL),
(10047, '14:00:00', '2019-10-18', 180, 100, 101, NULL),
(10048, '14:00:00', '2019-10-25', 180, 100, 101, NULL),
(10049, '14:00:00', '2019-11-01', 180, 100, 101, NULL),
(10050, '14:00:00', '2019-11-08', 180, 100, 101, NULL),
(10051, '14:00:00', '2019-11-15', 180, 100, 101, NULL),
(10052, '14:00:00', '2019-11-22', 180, 100, 101, NULL),
(10053, '14:00:00', '2019-11-29', 180, 100, 101, NULL),
(10054, '14:00:00', '2019-12-06', 180, 100, 101, NULL),
(10055, '14:00:00', '2019-12-13', 180, 100, 101, NULL),
(10056, '14:00:00', '2019-12-20', 180, 100, 101, NULL),
(10057, '14:00:00', '2019-12-27', 180, 100, 101, NULL),
(10058, '14:30:00', '2019-05-15', 120, 100, 104, NULL),
(10089, '14:30:00', '2024-07-31', 120, 100, 201, NULL);

INSERT INTO planned_unavailability (planned_unavailability_id, hour, day, duration, customer_id, user_id, reason, comment) VALUES
(100, '09:30:00', '2019-01-01', 150, 100, 101, 'meeting', NULL),
(101, '09:30:00', '2019-01-02', 150, NULL, 101, 'absence', 'Super commentaire'),
(102, '09:30:00', '2019-01-03', 150, 100, 101, 'other', 'Commentaire'),
(103, '09:30:00', '2019-05-30', 180, 100, 101, 'meeting', 'Autre commentaire mémorable');

INSERT INTO planning (planning_id, hour, duration, frequency, frequency_number, start, stop, generated_until, customer_id, user_id) VALUES
(100, '09:30:00', 150, 'weekly', 100, '2019-01-01', NULL, '2019-06-04', 100, 101),
(101, '14:00:00', 180, 'weekly', 100, '2019-05-03', '2019-12-31', '2020-01-03', 100, 101),
(102, '05:00:00', 60, 'monthly', 100, '2019-12-03', '2019-12-31', NULL, 100, 101);

INSERT INTO software (software_id, customer_id, software_name, software_login, software_password) VALUES
(100, 100, 'Ameli', 'bbb', 'bbb'),
(101, 100, 'Harmonie', 'aaa', 'aaa');

INSERT INTO invoice (invoice_id, contract_id, provider_id, customer_id, date, interval_start, interval_end, payment_date, email_delivery_date,  email_delivery_recipient, to_debit) VALUES
(100, 100, 100, 100, '2019-02-01', '2019-01-01', '2019-01-31', '2019-01-11', '2019-01-01', 'adel@example.com', true),
(101, 102, 100, 101, '2019-02-01', '2019-01-01', '2019-01-31', '2019-01-13', NULL, NULL, true),
(102, 103, 100, 102, '2020-01-01', '2019-12-01', '2019-12-31', '2020-01-15', NULL, NULL, true),
(103, 104, 100, 103, '2020-02-01', '2020-01-01', '2020-01-31', NULL, NULL, NULL, true),
(104, 105, 100, 104, '2020-12-31', '2020-11-01', '2020-11-30', '2020-12-11', NULL, NULL, true),
(105, 101, 100, 100, '2021-02-01', '2021-01-01', '2021-01-31', '2021-01-11', NULL, NULL, true),
(106, 102, 100, 101, '2021-02-01', '2021-01-01', '2021-01-31', '2021-01-13', NULL, NULL, false),
(107, 103, 100, 102, '2021-02-01', '2021-01-01', '2021-01-31', '2021-01-15', NULL, NULL, true),
(108, 104, 100, 103, '2021-02-01', '2021-01-01', '2021-01-31', NULL, NULL, NULL, true),
(109, 105, 100, 104, '2021-02-01', '2021-01-01', '2021-01-31', '2021-01-11', NULL, NULL, true),
(110, 100, 100, 100, '2023-01-15', '2023-01-01', '2023-01-31', '2023-01-20', NULL, NULL, true),
(111, 100, 100, 100, '2023-01-15', '2023-01-01', '2023-01-31', '2023-01-20', NULL, NULL, true),
(112, 100, 100, 100, '2023-01-15', '2023-01-01', '2023-01-31', '2023-01-20', NULL, NULL, true),
(113, 201, 201, 201,  '2019-02-01', '2019-01-01', '2019-01-31', '2019-01-11', NULL, NULL, true);

INSERT INTO invoice_line (invoice_line_id, label, unit_price, quantity, invoice_id, tax) VALUES
(100, 'Abonnement supplémentaire', 30, 1, 100, 20),
(101, 'Gestion du tiers-payant', 40, 5, 100, 20),
(102, 'Abonnement supplémentaire', 40, 10, 101, 8.5),
(103, 'Gestion du tiers-payant', 40, 5, 101, 8.5),
(104, 'Abonnement supplémentaire', 32, 10, 102, 20),
(105, 'Gestion du tiers-payant', 25, 3, 102, 20),
(106, 'Abonnement supplémentaire', 13, 10, 103, 20),
(107, 'Gestion du tiers-payant', 29, 3, 103, 20),
(108, 'Abonnement supplémentaire', 26, 10, 104, 0),
(109, 'Gestion du tiers-payant', 19, 3, 104, 0),
(110, 'Abonnement supplémentaire', 30, 1, 105, 20),
(111, 'Gestion du tiers-payant', 40, 5, 105, 20),
(112, 'Abonnement supplémentaire', 40, 10, 106, 8.5),
(113, 'Gestion du tiers-payant', 40, 5, 106, 8.5),
(114, 'Abonnement supplémentaire', 32, 10, 107, 20),
(115, 'Gestion du tiers-payant', 25, 3, 107, 20),
(116, 'Abonnement supplémentaire', 13, 10, 108, 20),
(117, 'Gestion du tiers-payant', 29, 3, 108, 20),
(118, 'Abonnement supplémentaire', 26, 10, 109, 0),
(119, 'Gestion du tiers-payant', 19, 3, 109, 0),
(120, 'Abonnement logiciel', 9.9, 69, 110, 20),
(123, 'Avoir forfait mensuel de gestion du tiers-payant', -142.9, 2, 110, 20),
(124, 'Courriers expédiés', 1.29, 26, 110, 20),
(125, 'Délégation', 42.39, 38, 110, 20),
(126, 'Délégation à l''heure', 40.11, 106.5, 110, 20),
(127, 'Forfait mensuel de gestion du tiers-payant', 295.92, 53, 110, 20),
(130, 'Forfait mensuel de gestion du tiers-payant - report', 292.28, 1, 110, 20),
(131, 'Relances des impayés', 37.00, 20, 110, 20),
(132, 'Remise commerciale exceptionnelle', -114.48, 2, 110, 20),
(133, 'Remise commerciale supplémentaire', -7.61, 4, 110, 20),
(121, 'Abonnement logiciel', 9.90, 1, 111, 8.5),
(128, 'Forfait mensuel de gestion du tiers-payant', 97.43, 1, 111, 8.5),
(122, 'Abonnement logiciel', 9.9, 3, 112, 0),
(129, 'Forfait mensuel de gestion du tiers-payant', 276.04, 3, 112, 0),
(201, 'Forfait mensuel de gestion du tiers-payant', 69.42, 3, 113, 0);

INSERT INTO unit_invoice_line (unit_invoice_line_id, invoice_id, label, unit_price, quantity, tax, customer_id) VALUES
(100, NULL, 'Super Service', 30, 1, 20, 101),
(101, 100, 'Abonnement supplémentaire', 30, 1, 20, 100),
(102, 101, 'Abonnement supplémentaire', 30, 1, 20, 101),
(103, NULL, 'Service supplémentaire', 30, 1, 20, 103);

INSERT INTO reminder (reminder_id, "date", "comment", treatment_date, author_id, customer_id, fse_number) VALUES
(100, '2019-03-02', 'à se souvenir', NULL, 102, 100, '123456789'),
(101, '2019-03-02', 'à se souvenir une nouvelle fois', NULL, 101, 100, '123456789');

INSERT INTO creditor_bank (creditor_bank_id, name, iban, bic) VALUES
(100, 'BRA', 'FR0414508000301716793327B47', 'RALPFR2G'),
(101, 'BNP', 'FR0717569000301954931722S91', 'BNPAFRPPXXX');

INSERT INTO estimate (estimate_id, user_id, prospect, date, balance_two_year, rejects_three_month, emitted_invoices_three_month, estimate_weekly_hours, corrected_estimate_weekly_hours) VALUES
(100, 100, 'ABC', '2019-03-02', 3596, 93, 2270, 7, 7),
(101, 100, 'EFG', '2018-04-15', 24510, 191, 4315, 24, 24),
(102, 100, 'HIJ', '2021-06-23', 14000, 116, 4424, 18, 18);

INSERT INTO rejection (rejection_id, finess, lot_number, fse_number, recycling, "date", "message", ro_fund, ro_claimed, ro_paid, rc_fund, rc_claimed, rc_paid, "code") VALUES
(100, '382918343', '1', '1', 1, '2024-04-26', 'LE NUMERO DE PRESCRIPTEUR EST INCONNU AU', '123456789', 100, 0, '987654321', 70, 0, 'RO'),
(101, '382918343', '1', '2', 4, '2023-04-26', 'FACTURE EN COURS DE TRAITEMENT CAISSE', '123456789', 50, 50, '987654321', 30, 0, 'RC'),
(102, '382918343', '1', '3', 1, '2022-04-26', 'L ETABLISSEMENT PRESCRIPTEUR EST INCONNU', '123456789', 10, 0, '', 5, 0, 'RO'),
(103, '382918343', '1', '4', 2, '2024-05-01', 'DROIT NON OUVERT EN R.C. A LA MUT', '123456789', 25, 25, '', 15, 0, 'RC'),
(104, '382918343', '1', '5', 1, '2024-03-30', 'RISQUE NON COUVERT', '123456789', 2.26, 2.26, '', 0.75, 0, 'RC');

INSERT INTO comment (date, title, text, author_id, customer_id) VALUES
(
'2022-04-26',
'Horaires d''accès au concentrateur', 'Suite au message du **titulaire**,


Se connecter seulement de 9h à midi à l''adresse suivante :
https://concentrateur1.fr',
100,
101
);

INSERT INTO user_healthcare_software (user_id, healthcare_software_id) VALUES
(100, 100),
(100, 101),
(104, 101),
(106, 100),
(201, 100);


COMMIT;
