from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Subject, Base, Course, User

engine = create_engine('sqlite:///categories.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

User1 = User(name="Dr Strange", email="stevenstrange@kamartaj.com",
             picture="https://cnet1.cbsistatic.com/img/OKR2sNNACWPsltN4y5i13tk"
                     "9biw=/936x527/2016/10/24/4c7b8f36-6f0e-427b-9884-59e1f72"
                     "09591/strange1.jpg")

session.add(User1)
session.commit()

subject1 = Subject(user_id=1, name="Physics")

session.add(subject1)
session.commit()

course1 = Course(user_id=1, name="Algebra-Baed Physics 1",
                 summary="Newtonian mechanics and waves.", subject=subject1)

session.add(course1)
session.commit()

course2 = Course(user_id=1, name="Algebra-Based Physics 2",
                 summary="Electricity, magnetism, and light", subject=subject1)

session.add(course2)
session.commit()

course3 = Course(user_id=1, name="Calculus-Based Physics 1",
                 summary="Newtonian mechanics, waves, and thermodynamics",
                 subject=subject1)

session.add(course3)
session.commit()

course4 = Course(user_id=1, name="Calculus-Based Physics 2",
                 summary="Electricity, magnetism, and light", subject=subject1)

session.add(course4)
session.commit()


subject2 = Subject(user_id=1, name="Biology")

session.add(subject2)
session.commit()

course1 = Course(user_id=1, name="Principles of Biology 1",
                 summary="Principles of chemistry, cellular, molecular, and "
                         "evolutionary biology, and the diversity of life",
                 subject=subject2)

session.add(course1)
session.commit()

course2 = Course(user_id=1, name="Principles of Biology 2",
                 summary="Development, structure, and function of both plant "
                         "and animals, and ecology",
                 subject=subject2)

session.add(course2)
session.commit()

course3 = Course(user_id=1, name="Human Anatomy and Physiology 1",
                 summary="Integumentary, skeletal, muscular, nervous, "
                         "endocrine, and sensory systems",
                 subject=subject2)

session.add(course3)
session.commit()

course4 = Course(user_id=1, name="Human Anatomy and Physiology 2",
                 summary="Digestive, circulatory, respiratory, urinary, and "
                         "reproductive systems",
                 subject=subject2)

session.add(course4)
session.commit()


subject3 = Subject(user_id=1, name="Chemistry")

session.add(subject3)
session.commit()

course1 = Course(user_id=1, name="General Chemistry 1",
                 summary="Chemical reactions, gas laws, chemical "
                         "nomenclature, structure of atoms, chemical bonding, "
                         "and solutions",
                 subject=subject3)

session.add(course1)
session.commit()

course2 = Course(user_id=1, name="General Chemistry 2",
                 summary="Chemical equilibria, kinetics, electrochemistry, "
                         "chemical compounds, and reactions, qualitative "
                         "analysis of ions, organic chemistry, and nuclear "
                         "chemistry",
                 subject=subject3)

session.add(course2)
session.commit()

course3 = Course(user_id=1, name="Physical Chemistry Lecture 1",
                 summary="Modern thermodynamics, and chemical kinetics, and "
                         "their applications.",
                 subject=subject3)

session.add(course3)
session.commit()

course4 = Course(user_id=1, name="Physical Chemistry Lecture 2",
                 summary="Quantum theory, lasers, spectroscopy, molecular "
                         "transport, and molecular reaction dynamics",
                 subject=subject3)

session.add(course4)
session.commit()


subject4 = Subject(user_id=1, name="Mathematics")

session.add(subject4)
session.commit()

course1 = Course(user_id=1, name="Calculus and Analytic Geometry 1",
                 summary="Real numbers, functions, limits, continuity, "
                         "derivatives, integrals, and applications",
                 subject=subject4)

session.add(course1)
session.commit()

course2 = Course(user_id=1, name="Calculus and Analytic Geometry 2",
                 summary="Conic sections, transcendental functions, techniques"
                         " of integration, indeterminate forms, improper "
                         "integrals, and infinite series",
                 subject=subject4)

session.add(course2)
session.commit()

course3 = Course(user_id=1, name="Calculus and Analytic Geometry 3",
                 summary="Three-dimensional analytic geometry, vectors, "
                         "partial derivatives, multiple integrals, line "
                         "integrals, and surface integrals",
                 subject=subject4)

session.add(course3)
session.commit()

course4 = Course(user_id=1, name="Introduction to Abstract Mathematics",
                 summary="Fundamentals of formal mathematics emphasizing "
                         "mathematical writing and types of formal proof.",
                 subject=subject4)

session.add(course4)
session.commit()
